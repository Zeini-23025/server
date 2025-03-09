from django.db import models, transaction
from datetime import timedelta
from users.models import User
from django.utils.crypto import get_random_string
from getionEmploi.utils import envoyer_email
from django.core.exceptions import ValidationError

class Enseignant(models.Model):
    nom = models.CharField(max_length=255)
    identifiant = models.CharField(max_length=255, unique=True, null=False)
    email = models.EmailField(unique=True, max_length=255, null=False)

    def get_disponibilites(self):
        return list(self.disponibilites.values('jour', 'creneau'))
    
    def __str__(self):
        return self.nom

    def save(self, *args, **kwargs):
        
        with transaction.atomic():
            is_new = self.pk is None  
            super().save(*args, **kwargs)

            if is_new:
                password = get_random_string()  
                if envoyer_email(self.email, password, "Votre mot de passe"):
                    User.objects.create_user(
                        email=self.email,
                        password=password
                    )


class Matiere(models.Model):
    code = models.CharField(max_length=50, unique=True)
    nom = models.CharField(max_length=255)
    credits = models.IntegerField()
    semestre = models.IntegerField()
    filiere = models.CharField(max_length=255)

    def __str__(self):
        return self.nom
    def get_enseignants(self):
        return list(self.affectationenseignant_set.values_list('enseignant__nom', flat=True))


class Groupe(models.Model):

    nom = models.CharField(max_length=255, unique=True)
    semestre = models.IntegerField()

    parent = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True, related_name='sous_groupes'
    )
    def get_matieres(self):
        return list(self.groupe_matiere_set.values_list('matiere__nom', flat=True))
    def __str__(self):
        return self.nom
    
class Salle(models.Model):
    nom = models.CharField(max_length=255, unique=True)
    TYPE_SALLE = [
        ('CM', 'Cours Magistral'),
        ('TD', 'Travaux Dirigés'),
        ('TP', 'Travaux Pratiques'),
    ]
    type_salle = models.CharField(max_length=2, choices=TYPE_SALLE)

    def __str__(self):
        return f"{self.nom} - {self.type_salle}"

class Disponibilite(models.Model):
    enseignant = models.ForeignKey(Enseignant, on_delete=models.CASCADE, related_name="disponibilites")
    jour = models.CharField(max_length=10, choices=[
        ('Lundi', 'Lundi'), ('Mardi', 'Mardi'), ('Mercredi', 'Mercredi'), 
        ('Jeudi', 'Jeudi'), ('Vendredi', 'Vendredi'), ('Samedi', 'Samedi')
    ])
    creneau = models.CharField(max_length=2, choices=[
        ('P1', 'P1'), ('P2', 'P2'), ('P3', '3'),
        ('P4', 'P4'), ('P5', 'P5'), ('P6', 'P6')
    ])
    semaine = models.DateField()

    class Meta:
        unique_together = ('enseignant', 'jour', 'creneau', 'semaine')

    def __str__(self):
        return f"{self.enseignant} - {self.jour} {self.creneau} (Semaine {self.semaine})"
    
class GroupeMatiere(models.Model):
    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE)
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('groupe', 'matiere')


class ChargeHebdomadaire(models.Model):
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)
    heures_cm = models.IntegerField(default=0)
    heures_td = models.IntegerField(default=0)
    heures_tp = models.IntegerField(default=0)
    semaine = models.DateField()
    reconduction_de = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True, related_name='reconductions'
    )

    def __str__(self):
        return f"{self.matiere} - {self.semaine} (CM: {self.heures_cm}, TD: {self.heures_td}, TP: {self.heures_tp})"

    def reconduire_configuration(self):
        """ Permet de reconduire la configuration de la semaine précédente """
        semaine_precedente = self.semaine - timedelta(days=7)
        try:
            charge_precedente = ChargeHebdomadaire.objects.get(matiere=self.matiere, semaine=semaine_precedente)
            self.heures_cm = charge_precedente.heures_cm
            self.heures_td = charge_precedente.heures_td
            self.heures_tp = charge_precedente.heures_tp
            self.reconduction_de = charge_precedente
            self.save()
            return True
        except ChargeHebdomadaire.DoesNotExist:
            return False


class AffectationEnseignant(models.Model):
    TYPE_COURS = [
        ('CM', 'Cours Magistral'),
        ('TD', 'Travaux Dirigés'),
        ('TP', 'Travaux Pratiques'),
    ]

    enseignant = models.ForeignKey(Enseignant, on_delete=models.CASCADE)
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)
    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE)
    type_cours = models.CharField(max_length=2, choices=TYPE_COURS)
    jour = models.CharField(max_length=10, choices=[
        ('Lundi', 'Lundi'), ('Mardi', 'Mardi'), ('Mercredi', 'Mercredi'), 
        ('Jeudi', 'Jeudi'), ('Vendredi', 'Vendredi'), ('Samedi', 'Samedi')
    ])
    creneau = models.CharField(max_length=2, choices=[
        ('P1', 'P1'), ('P2', 'P2'), ('P3', 'P3'),
        ('P4', 'P4'), ('P5', 'P5'), ('P6', 'P6')
    ])

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['enseignant', 'jour', 'creneau'], name='unique_enseignant_creneau_affectation'),
        ]

    def clean(self):
        """ Vérifier si l'enseignant est disponible et n'a pas de conflit d'affectation """
        # Vérifier la disponibilité
        if not Disponibilite.objects.filter(enseignant=self.enseignant, jour=self.jour, creneau=self.creneau).exists():
            raise ValidationError("L'enseignant n'est pas disponible pour ce créneau.")

        # Vérifier si l'enseignant a déjà un cours affecté à ce créneau
        if AffectationEnseignant.objects.filter(enseignant=self.enseignant, jour=self.jour, creneau=self.creneau).exists():
            raise ValidationError("L'enseignant est déjà affecté à un autre cours sur ce créneau.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.enseignant} - {self.matiere} ({self.type_cours}) [{self.jour}, {self.creneau}]"


class Calendrier(models.Model):
    semaine = models.DateField()
    jour = models.CharField(max_length=20, choices=[
        ('Lundi', 'Lundi'), ('Mardi', 'Mardi'), ('Mercredi', 'Mercredi'), 
        ('Jeudi', 'Jeudi'), ('Vendredi', 'Vendredi'), ('Samedi', 'Samedi')
    ])
    nb_creneaux = models.IntegerField(default=5)  # Par défaut, 5 créneaux par jour
    exception = models.BooleanField(default=False)  # True si jour férié ou événement spécial
    creneaux_exceptionnels = models.JSONField(blank=True, null=True)  # Liste des créneaux exceptionnels

    class Meta:
        unique_together = ('semaine', 'jour')

    def __str__(self):
        return f"{self.jour} (Semaine {self.semaine}) - {'Exception' if self.exception else 'Normal'}"



class EmploiTemps(models.Model):
    CRENEAUX = [
        ('P1', 'Période 1'),
        ('P2', 'Période 2'),
        ('P3', 'Période 3'),
        ('P4', 'Période 4'),
        ('P5', 'Période 5'),
        ('P6', 'Période 6'),
    ]

    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE)
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)
    enseignant = models.ForeignKey(Enseignant, on_delete=models.CASCADE)
    salle = models.ForeignKey(Salle, on_delete=models.CASCADE, null=True, blank=True)  # ✅ Ajout de la salle
    jour = models.CharField(max_length=10, choices=[
        ('Lundi', 'Lundi'), ('Mardi', 'Mardi'), ('Mercredi', 'Mercredi'),
        ('Jeudi', 'Jeudi'), ('Vendredi', 'Vendredi'), ('Samedi', 'Samedi')
    ])
    creneau = models.CharField(max_length=2, choices=CRENEAUX)
    type_cours = models.CharField(max_length=50)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['enseignant', 'jour', 'creneau'], name='unique_enseignant_creneau_emploi'),
            models.UniqueConstraint(fields=['groupe', 'jour', 'creneau'], name='unique_groupe_creneau'),
            models.UniqueConstraint(fields=['salle', 'jour', 'creneau'], name='unique_salle_creneau'),  # ✅ Ajout de la contrainte
        ]

    def clean(self):
        """
        Vérifie si l'enseignant, le groupe ou la salle est déjà occupé sur ce créneau.
        """
        # Vérifier si l'enseignant est déjà occupé
        if EmploiTemps.objects.filter(enseignant=self.enseignant, jour=self.jour, creneau=self.creneau).exists():
            raise ValidationError("L'enseignant a déjà un cours sur ce créneau.")

        # Vérifier si le groupe est déjà occupé
        if EmploiTemps.objects.filter(groupe=self.groupe, jour=self.jour, creneau=self.creneau).exists():
            raise ValidationError("Le groupe a déjà un cours sur ce créneau.")

        # Vérifier si la salle est déjà occupée
        if self.salle and EmploiTemps.objects.filter(salle=self.salle, jour=self.jour, creneau=self.creneau).exists():
            raise ValidationError("Cette salle est déjà réservée pour un autre cours à ce créneau.")

    def save(self, *args, **kwargs):
        """
        Applique les vérifications avant de sauvegarder.
        """
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.groupe.nom} - {self.matiere.nom} ({self.jour}, {self.creneau}) - {self.salle.nom if self.salle else 'Salle Non Assignée'}"
        
class ContrainteHoraire(models.Model):
    """
    Modèle permettant de fixer un créneau spécifique pour une matière et un groupe.
    Exemple : "Le cours d'Anglais pour G1 doit toujours être le mardi en P2."
    """
    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE)
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)
    jour = models.CharField(max_length=10, choices=[
        ('Lundi', 'Lundi'), ('Mardi', 'Mardi'), ('Mercredi', 'Mercredi'),
        ('Jeudi', 'Jeudi'), ('Vendredi', 'Vendredi'), ('Samedi', 'Samedi')
    ])
    creneau = models.CharField(max_length=2, choices=[
        ('P1', 'Période 1'),
        ('P2', 'Période 2'),
        ('P3', 'Période 3'),
        ('P4', 'Période 4'),
        ('P5', 'Période 5'),
        ('P6', 'Période 6'),
    ])

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['groupe', 'matiere', 'jour', 'creneau'], name='unique_contrainte_horaire')
        ]

    def __str__(self):
        return f"{self.matiere.nom} - {self.groupe.nom} ({self.jour}, {self.creneau})"

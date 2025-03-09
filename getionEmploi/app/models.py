from django.db import models
from django.db import models, transaction
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from users.models import User
from getionEmploi.utils import envoyer_email

class Enseignant(models.Model):
    nom = models.CharField(max_length=255)
    identifiant = models.CharField(max_length=255, unique=True,null=False)
    email = models.EmailField(unique=True, max_length=255, null=False)
    
    def __str__(self):
        return self.nom

    def save(self, *args, **kwargs):
        with transaction.atomic():
            is_new = self.pk is None  
            super().save(*args, **kwargs) 
            
            if is_new: 
                # password = get_random_string(6)
                password = "1234"
                if envoyer_email(self.email,password,"votre mot de passe"):
                    User.objects.create_user(
                        id_enseignt=self.pk,
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


class Groupe(models.Model):
    nom = models.CharField(max_length=255)
    semestre = models.IntegerField()

    def __str__(self):
        return self.nom


class ChargeHebdomadaire(models.Model):
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)
    heures_cm = models.IntegerField()
    heures_td = models.IntegerField()
    heures_tp = models.IntegerField()
    semaine = models.IntegerField()


class AffectationEnseignant(models.Model):
    enseignant = models.ForeignKey(Enseignant, on_delete=models.CASCADE)
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)
    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE)
    type_cours = models.CharField(max_length=50, choices=[('CM', 'Cours Magistral'), ('TD', 'Travaux Dirigés'), ('TP', 'Travaux Pratiques')])

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['matiere', 'groupe', 'type_cours'],
                name='unique_matiere_groupe_typecours'
            )
        ]

class Calendrier(models.Model):
    semaine = models.IntegerField()
    jour = models.CharField(max_length=20)
    nb_creneaux = models.IntegerField()


class EmploiTemps(models.Model):
    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE)
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)
    enseignant = models.ForeignKey(Enseignant, on_delete=models.CASCADE)
    jour = models.CharField(max_length=50)
    creneau = models.CharField(max_length=50, choices=[
        ('P1', 'Période 1'),
        ('P2', 'Période 2'),
        ('P3', 'Période 3'),
        ('P4', 'Période 4'),
        ('P5', 'Période 5'),
        ('P6', 'Période 6')
    ])
    type_cours = models.CharField(max_length=50)


class DisponibiliteEnseignant(models.Model):
    enseignant = models.ForeignKey(Enseignant, on_delete=models.CASCADE)
    jour = models.CharField(max_length=50)
    creneau = models.CharField(max_length=50)
    semaine = models.IntegerField()


class GroupeMatiere(models.Model):
    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE)
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)


class ExceptionCalendrier(models.Model):
    semaine = models.IntegerField()
    jour = models.CharField(max_length=50)
    type_exception = models.CharField(max_length=50)
    valeur = models.CharField(max_length=255)


class ConflitGroupe(models.Model):
    groupe1 = models.ForeignKey(Groupe, on_delete=models.CASCADE, related_name='conflits_groupe1')
    groupe2 = models.ForeignKey(Groupe, on_delete=models.CASCADE, related_name='conflits_groupe2')
    raison = models.CharField(max_length=255)

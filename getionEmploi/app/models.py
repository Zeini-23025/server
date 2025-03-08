from django.db import models


class Enseignant(models.Model):
    nom = models.CharField(max_length=255)
    identifiant = models.CharField(max_length=255, unique=True)

<<<<<<< HEAD
=======

>>>>>>> yeslem
    def __str__(self):
        return self.nom


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
    type_cours = models.CharField(max_length=50)


class EmploiTemps(models.Model):
    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE)
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)
    enseignant = models.ForeignKey(Enseignant, on_delete=models.CASCADE)
    jour = models.CharField(max_length=50)
    creneau = models.CharField(max_length=50)
    type_cours = models.CharField(max_length=50)
    semaine = models.IntegerField()


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

from rest_framework import serializers
from .models import Matiere ,EmploiTemps ,Groupe ,Enseignant ,Disponibilite ,Calendrier ,ChargeHebdomadaire ,AffectationEnseignant ,GroupeMatiere ,ContrainteHoraire

class MatiereSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matiere

class EnseignantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enseignant
        fields = '__all__'

class GroupeSerializer(serializers.ModelSerializer):
    sous_groupes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Groupe
        fields = ['id', 'nom', 'semestre', 'parent', 'sous_groupes']
        
class DisponibiliteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disponibilite
        fields = ['id', 'enseignant', 'jour', 'creneau', 'semaine']
        
class CalendrierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calendrier
        fields = ['id', 'semaine', 'jour', 'nb_creneaux', 'exception', 'creneaux_exceptionnels']
        
        
class ChargeHebdomadaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChargeHebdomadaire
        fields = ['id', 'matiere', 'heures_cm', 'heures_td', 'heures_tp', 'semaine', 'reconduction_de']

class AffectationEnseignantSerializer(serializers.ModelSerializer):
    class Meta:
        model = AffectationEnseignant
        fields = ['id', 'enseignant', 'matiere', 'groupe', 'type_cours', 'jour', 'creneau']

    def validate(self, data):
        """ Vérifie si l'enseignant est disponible et s'il n'y a pas de conflit """
        enseignant = data['enseignant']
        jour = data['jour']
        creneau = data['creneau']

        # Vérifier la disponibilité de l'enseignant
        if not enseignant.disponibilites.filter(jour=jour, creneau=creneau).exists():
            raise serializers.ValidationError("L'enseignant n'est pas disponible pour ce créneau.")

        # Vérifier s'il est déjà affecté à un autre cours
        if AffectationEnseignant.objects.filter(enseignant=enseignant, jour=jour, creneau=creneau).exists():
            raise serializers.ValidationError("L'enseignant est déjà affecté à un autre cours sur ce créneau.")

        return data
    
class GroupeMatiereSerializer(serializers.ModelSerializer):
    groupe = serializers.PrimaryKeyRelatedField(queryset=Groupe.objects.all())
    matiere = serializers.PrimaryKeyRelatedField(queryset=Matiere.objects.all())

    class Meta:
        model = GroupeMatiere
        fields = ['id', 'groupe', 'matiere']

    def create(self, validated_data):
        groupe = validated_data['groupe']
        matiere = validated_data['matiere']
        
        # Vérifier si la relation existe déjà
        if GroupeMatiere.objects.filter(groupe=groupe, matiere=matiere).exists():
            raise serializers.ValidationError("Ce groupe est déjà associé à cette matière.")
        
        return GroupeMatiere.objects.create(**validated_data)


class ContrainteHoraireSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContrainteHoraire
        fields = ['id', 'groupe', 'matiere', 'jour', 'creneau']

    def validate(self, data):
        """ Empêcher les doublons """
        if ContrainteHoraire.objects.filter(
            groupe=data['groupe'], matiere=data['matiere'], jour=data['jour'], creneau=data['creneau']
        ).exists():
            raise serializers.ValidationError("Une contrainte existe déjà pour ce groupe et cette matière.")
        return data
    
class EmploiTempsSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = EmploiTemps
        fields = ['id', 'groupe', 'matiere', 'enseignant', 'jour', 'creneau', 'type_cours']

    def validate(self, data):
        """
        Vérifie s'il y a des conflits avant d'ajouter un emploi du temps.
        """
        enseignant = data['enseignant']
        groupe = data['groupe']
        jour = data['jour']
        creneau = data['creneau']

        # Vérifier si l'enseignant est déjà occupé à ce créneau
        if EmploiTemps.objects.filter(enseignant=enseignant, jour=jour, creneau=creneau).exists():
            raise serializers.ValidationError("L'enseignant a déjà un cours sur ce créneau.")

        # Vérifier si le groupe a déjà un cours sur ce créneau
        if EmploiTemps.objects.filter(groupe=groupe, jour=jour, creneau=creneau).exists():
            raise serializers.ValidationError("Le groupe a déjà un cours sur ce créneau.")

        return data


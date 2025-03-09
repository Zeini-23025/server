from rest_framework import serializers
from .models import Matiere , AffectationEnseignant ,EmploiTemps

class MatiereSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matiere

class EnseignantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enseignant
        fields = '__all__'

class AffectationEnseignantSerializer(serializers.ModelSerializer):
    class Meta:
        model = AffectationEnseignant
        fields = '__all__'  

    def validate(self, data):
        """ Vérifie l'unicité de (matiere, groupe, type_cours). """
        matiere = data.get('matiere')
        groupe = data.get('groupe')
        type_cours = data.get('type_cours')

        if AffectationEnseignant.objects.filter(
            matiere=matiere, groupe=groupe, type_cours=type_cours
        ).exists():
            raise serializers.ValidationError(
                "Un enseignant est déjà affecté à cette matière, ce groupe et ce type de cours."
            )

        return data

class EmploiTempsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmploiTemps
        fields = '__all__'  

    def validate(self, data):
        enseignant = data.get('enseignant')
        matiere = data.get('matiere')
        semaine = data.get('semaine')
        jour = data.get('jour')
        creneau = data.get('creneau')
        
        if EmploiTemps.objects.filter(
            enseignant=enseignant, 
            matiere=matiere, 
            semaine=semaine, 
            jour=jour, 
            creneau=creneau
        ).exists():
            raise serializers.ValidationError(
                "Cet enseignant est déjà affecté à cette matière pour ce créneau et ce jour."
            )
        
        return data

from rest_framework import serializers
from .models import Matiere, Enseignant, ChargeHebdomadaire, EmploiTemps

class MatiereSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matiere
        fields = '__all__'

class EnseignantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enseignant
        fields = '__all__'

class ChargeHebdomadaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChargeHebdomadaire
        fields = '__all__'

class EmploiTempsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmploiTemps
        fields = '__all__'
from rest_framework import serializers
from .models import Matiere

class MatiereSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matiere
from .models import Enseignant

class EnseignantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enseignant
        fields = '__all__'

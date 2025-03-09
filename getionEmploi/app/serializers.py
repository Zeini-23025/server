from rest_framework import serializers
from .models import Enseignant, Groupe, GroupeMatiere, ConflitGroupe, Matiere

class MatiereSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matiere
        fields = '__all__'

class EnseignantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enseignant
        fields = '__all__'

class GroupeSerializer(serializers.ModelSerializer):
    matieres = serializers.SerializerMethodField()
    conflits = serializers.SerializerMethodField()

    class Meta:
        model = Groupe
        fields = ['id', 'nom', 'semestre', 'matieres', 'conflits']

    def get_matieres(self, obj):
        """Retourne la liste des matières liées à ce groupe"""
        matieres = Matiere.objects.filter(groupematiere__groupe=obj)
        return MatiereSerializer(matieres, many=True).data

    def get_conflits(self, obj):
        """Retourne la liste des groupes en conflit avec ce groupe"""
        conflits = ConflitGroupe.objects.filter(groupe1=obj) | ConflitGroupe.objects.filter(groupe2=obj)
        groupes = {c.groupe1 if c.groupe2 == obj else c.groupe2 for c in conflits}
        return [g.nom for g in groupes]

class GroupeMatiereSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupeMatiere
        fields = '__all__'

class ConflitGroupeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConflitGroupe
        fields = '__all__'

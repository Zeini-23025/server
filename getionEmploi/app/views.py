from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import (
    Matiere, 
    Enseignant, 
    Groupe, 
    GroupeMatiere, 
    ConflitGroupe
)
from .serializers import (
    MatiereSerializer, 
    EnseignantSerializer,
    GroupeSerializer, 
    GroupeMatiereSerializer, 
    ConflitGroupeSerializer
)

class MatiereViewSet(viewsets.ModelViewSet):
    queryset = Matiere.objects.all()
    serializer_class = MatiereSerializer

class EnseignantViewSet(viewsets.ModelViewSet):
    queryset = Enseignant.objects.all()
    serializer_class = EnseignantSerializer

class GroupeViewSet(viewsets.ModelViewSet):
    queryset = Groupe.objects.all()
    serializer_class = GroupeSerializer

    @action(detail=True, methods=['post'])
    def ajouter_matiere(self, request, pk=None):
        """Ajoute une matière à un groupe"""
        groupe = self.get_object()
        matiere_id = request.data.get("matiere_id")

        try:
            matiere = Matiere.objects.get(id=matiere_id)
            GroupeMatiere.objects.create(groupe=groupe, matiere=matiere)
            return Response({"message": f"{matiere.nom} ajoutée à {groupe.nom}"})
        except Matiere.DoesNotExist:
            return Response({"error": "Matière introuvable"}, status=400)

    @action(detail=True, methods=['post'])
    def ajouter_conflit(self, request, pk=None):
        """Ajoute un conflit entre deux groupes"""
        groupe1 = self.get_object()
        groupe2_id = request.data.get("groupe2_id")

        try:
            groupe2 = Groupe.objects.get(id=groupe2_id)
            if groupe1 == groupe2:
                return Response({"error": "Un groupe ne peut pas être en conflit avec lui-même"}, status=400)

            ConflitGroupe.objects.create(groupe1=groupe1, groupe2=groupe2, raison="Cours en parallèle interdits")
            return Response({"message": f"Conflit ajouté entre {groupe1.nom} et {groupe2.nom}"})
        except Groupe.DoesNotExist:
            return Response({"error": "Groupe introuvable"}, status=400)

class GroupeMatiereViewSet(viewsets.ModelViewSet):
    queryset = GroupeMatiere.objects.all()
    serializer_class = GroupeMatiereSerializer

class ConflitGroupeViewSet(viewsets.ModelViewSet):
    queryset = ConflitGroupe.objects.all()
    serializer_class = ConflitGroupeSerializer
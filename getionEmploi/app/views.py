from rest_framework import viewsets
from .models import Matiere, Enseignant ,AffectationEnseignant
from .serializers import MatiereSerializer, EnseignantSerializer , AffectationEnseignantSerializer ,EmploiTempsSerializer

class MatiereViewSet(viewsets.ModelViewSet):
    queryset = Matiere.objects.all()
    serializer_class = MatiereSerializer

class EnseignantViewSet(viewsets.ModelViewSet):
    queryset = Enseignant.objects.all()
    serializer_class = EnseignantSerializer


class AffectationEnseignantViewSet(viewsets.ModelViewSet):
    queryset = AffectationEnseignant.objects.all()
    serializer_class = AffectationEnseignantSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        matiere = self.request.query_params.get('matiere')
        groupe = self.request.query_params.get('groupe')
        type_cours = self.request.query_params.get('type_cours')

        if matiere:
            queryset = queryset.filter(matiere=matiere)
        if groupe:
            queryset = queryset.filter(groupe=groupe)
        if type_cours:
            queryset = queryset.filter(type_cours=type_cours)

        return queryset


class EmploiTempsViewSet(viewsets.ModelViewSet):
    queryset = EmploiTemps.objects.all()
    serializer_class = EmploiTempsSerializer

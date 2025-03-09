from rest_framework import viewsets
from .models import Matiere, Enseignant, ChargeHebdomadaire, EmploiTemps
from .serializers import MatiereSerializer, EnseignantSerializer, ChargeHebdomadaireSerializer, EmploiTempsSerializer

class MatiereViewSet(viewsets.ModelViewSet):
    queryset = Matiere.objects.all()
    serializer_class = MatiereSerializer

class EnseignantViewSet(viewsets.ModelViewSet):
    queryset = Enseignant.objects.all()
    serializer_class = EnseignantSerializer

class ChargeHebdomadaireViewSet(viewsets.ModelViewSet):
    queryset = ChargeHebdomadaire.objects.all()
    serializer_class = ChargeHebdomadaireSerializer

class EmploiTempsViewSet(viewsets.ModelViewSet):
    queryset = EmploiTemps.objects.all()
    serializer_class = EmploiTempsSerializer
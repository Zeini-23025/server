from rest_framework import viewsets
from .models import Matiere, Enseignant
from .serializers import MatiereSerializer, EnseignantSerializer

class MatiereViewSet(viewsets.ModelViewSet):
    queryset = Matiere.objects.all()
    serializer_class = MatiereSerializer

class EnseignantViewSet(viewsets.ModelViewSet):
    queryset = Enseignant.objects.all()
    serializer_class = EnseignantSerializer

from rest_framework import viewsets
from .models import Enseignant
from .serializers import EnseignantSerializer

class EnseignantViewSet(viewsets.ModelViewSet):
    queryset = Enseignant.objects.all()
    serializer_class = EnseignantSerializer

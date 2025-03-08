from rest_framework import viewsets
from .models import Matiere
from .serializers import MatiereSerializer

class MatiereViewSet(viewsets.ModelViewSet):
    queryset = Matiere.objects.all()
    serializer_class = MatiereSerializer

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EnseignantViewSet
from .views import MatiereViewSet


router = DefaultRouter()
router.register(r'matieres', MatiereViewSet)
router.register(r'enseignants', EnseignantViewSet, basename='enseignant')

urlpatterns = [
    path('api/', include(router.urls)),  
]


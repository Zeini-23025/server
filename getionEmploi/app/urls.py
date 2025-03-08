from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EnseignantViewSet,GroupeViewSet, GroupeMatiereViewSet, ConflitGroupeViewSet

router = DefaultRouter()
router.register(r'enseignants', EnseignantViewSet, basename='enseignant')
router.register(r'groupes', GroupeViewSet)
router.register(r'groupe-matieres', GroupeMatiereViewSet)
router.register(r'conflit-groupes', ConflitGroupeViewSet)
urlpatterns = [
    path('', include(router.urls)),  
]

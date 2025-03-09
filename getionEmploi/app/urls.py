from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EnseignantViewSet, MatiereViewSet, ChargeHebdomadaireViewSet, EmploiTempsViewSet

router = DefaultRouter()
router.register(r'matieres', MatiereViewSet)
router.register(r'enseignants', EnseignantViewSet, basename='enseignant')
router.register(r'charge_hebdomadaire', ChargeHebdomadaireViewSet)
router.register(r'emploi_temps', EmploiTempsViewSet) 

urlpatterns = [
    path('api/', include(router.urls)),
]
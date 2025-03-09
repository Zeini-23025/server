from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EnseignantViewSet,
    MatiereViewSet,
    GroupeViewSet,
    GroupeMatiereViewSet,
    ConflitGroupeViewSet
)

router = DefaultRouter()
router.register(r'matieres', MatiereViewSet)
router.register(r'enseignants', EnseignantViewSet, basename='enseignant')
router.register(r'groupes', GroupeViewSet)
router.register(r'groupe-matieres', GroupeMatiereViewSet)
router.register(r'conflit-groupes', ConflitGroupeViewSet)

urlpatterns = [
    path('', include(router.urls)),  
    path('reconduire/', DisponibiliteViewSet.as_view({'post': 'reconduire_disponibilites'}), name="reconduire_disponibilites"),
    path('ajouter-exception/', CalendrierViewSet.as_view({'post': 'ajouter_exception'}), name="ajouter_exception"),
    path('supprimer-jour/', CalendrierViewSet.as_view({'post': 'supprimer_jour'}), name="supprimer_jour"),
    path('charges-reconduire/', ChargeHebdomadaireViewSet.as_view({'post': 'reconduire'}), name="reconduire_charges"),
    path('enseignants/<int:enseignant_id>/disponibilites/', get_enseignant_disponibilites, name='get_enseignant_disponibilites'),
    path('groupes/<int:groupe_id>/matieres/', get_groupe_matiere, name='get_groupe_matiere'),
    path('matieres/<int:matiere_id>/enseignants/', get_matiere_enseignants, name='get_matiere_enseignants'),
]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EnseignantViewSet,
    MatiereViewSet,
    GroupeViewSet,
    GroupeMatiereViewSet,
    ChargeHebdomadaireViewSet,
    DisponibiliteViewSet,
    CalendrierViewSet,
    AffectationEnseignantViewSet,
    ContrainteHoraireViewSet,
    get_enseignant_disponibilites,
    get_groupe_matiere,
    get_matiere_enseignants,
    SalleViewSet ,
     EmploiTempsGroupeViewSet,
    EmploiTempsEnseignantViewSet,
    GenererEmploiTempsViewSet,
)

router = DefaultRouter()
router.register(r'matieres', MatiereViewSet)
router.register(r'enseignants', EnseignantViewSet, basename='enseignant')
router.register(r'groupes', GroupeViewSet)
router.register(r'disponibilites', DisponibiliteViewSet)
router.register(r'calendrier', CalendrierViewSet)
router.register(r'charges', ChargeHebdomadaireViewSet)
router.register(r'affectations-enseignant', AffectationEnseignantViewSet)
router.register(r'groupes-matieres', GroupeMatiereViewSet)
router.register(r'contraintes_horaires', ContrainteHoraireViewSet)
router.register(r'salles', SalleViewSet)

urlpatterns = [
    path('', include(router.urls)),  
    path('reconduire/', DisponibiliteViewSet.as_view({'post': 'reconduire_disponibilites'}), name="reconduire_disponibilites"),
    path('ajouter-exception/', CalendrierViewSet.as_view({'post': 'ajouter_exception'}), name="ajouter_exception"),
    path('supprimer-jour/', CalendrierViewSet.as_view({'post': 'supprimer_jour'}), name="supprimer_jour"),
    path('charges-reconduire/', ChargeHebdomadaireViewSet.as_view({'post': 'reconduire'}), name="reconduire_charges"),
    path('enseignants/<int:enseignant_id>/disponibilites/', get_enseignant_disponibilites, name='get_enseignant_disponibilites'),
    path('groupes/<int:groupe_id>/matieres/', get_groupe_matiere, name='get_groupe_matiere'),
    path('matieres/<int:matiere_id>/enseignants/', get_matiere_enseignants, name='get_matiere_enseignants'),
    
    path('groupe/<int:groupe_id>/semaine/<str:semaine>/', EmploiTempsGroupeViewSet.as_view({'get': 'list'}), name='emploi-du-temps-groupe'),
    path('enseignant/<int:enseignant_id>/semaine/<str:semaine>/', EmploiTempsEnseignantViewSet.as_view({'get': 'list'}), name='emploi-du-temps-enseignant'),
    path('generer/', GenererEmploiTempsViewSet.as_view({'post': 'create'}), name='generer-emploi-du-temps'),
]

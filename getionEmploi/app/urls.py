from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EnseignantViewSet

router = DefaultRouter()
router.register(r'enseignants', EnseignantViewSet, basename='enseignant')

urlpatterns = [
    path('', include(router.urls)),  
]

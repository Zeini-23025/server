from rest_framework import viewsets
from datetime import timedelta
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Matiere, Enseignant ,Groupe ,Calendrier ,AffectationEnseignant ,GroupeMatiere ,ContrainteHoraire ,Disponibilite ,ChargeHebdomadaire ,EmploiTemps
from .serializers import MatiereSerializer, EnseignantSerializer ,GroupeSerializer,CalendrierSerializer ,DisponibiliteSerializer,AffectationEnseignantSerializer,GroupeMatiereSerializer,ChargeHebdomadaireSerializer ,ContrainteHoraireSerializer,EmploiTempsSerializer

class MatiereViewSet(viewsets.ModelViewSet):
    queryset = Matiere.objects.all()
    serializer_class = MatiereSerializer

class EnseignantViewSet(viewsets.ModelViewSet):
    queryset = Enseignant.objects.all()
    serializer_class = EnseignantSerializer



class GroupeViewSet(viewsets.ModelViewSet):
    queryset = Groupe.objects.all()
    serializer_class = GroupeSerializer

    def create(self, request, *args, **kwargs):
        """ Empêcher la création de doublons et valider les relations parent/enfant """
        parent_id = request.data.get('parent')
        semestre = request.data.get('semestre')

        # Vérifier si le groupe existe déjà
        if Groupe.objects.filter(nom=request.data.get('nom')).exists():
            return Response({'error': 'Ce groupe existe déjà.'}, status=status.HTTP_400_BAD_REQUEST)

        # Vérifier si le parent appartient au même semestre
        if parent_id:
            try:
                parent = Groupe.objects.get(id=parent_id)
                if parent.semestre != int(semestre):
                    return Response({'error': 'Le groupe parent doit être du même semestre.'}, status=status.HTTP_400_BAD_REQUEST)
            except Groupe.DoesNotExist:
                return Response({'error': 'Groupe parent non trouvé.'}, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)
    
class DisponibiliteViewSet(viewsets.ModelViewSet):
    queryset = Disponibilite.objects.all()
    serializer_class = DisponibiliteSerializer

    def create(self, request, *args, **kwargs):
        """ Empêcher les doublons et enregistrer une nouvelle disponibilité """
        enseignant = request.data.get('enseignant')
        jour = request.data.get('jour')
        creneau = request.data.get('creneau')
        semaine = request.data.get('semaine')

        if Disponibilite.objects.filter(enseignant=enseignant, jour=jour, creneau=creneau, semaine=semaine).exists():
            return Response({'error': 'Cet enseignant est déjà disponible sur ce créneau.'}, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)

    def reconduire_disponibilites(self, request):
        """ Reconduire les disponibilités d'une semaine précédente """
        semaine_actuelle = request.data.get('semaine_actuelle')
        semaine_precedente = semaine_actuelle - timedelta(days=7)
        enseignant_id = request.data.get('enseignant')

        # Vérifier si des disponibilités existent pour la semaine précédente
        anciennes_disponibilites = Disponibilite.objects.filter(enseignant=enseignant_id, semaine=semaine_precedente)
        if not anciennes_disponibilites.exists():
            return Response({'error': 'Aucune disponibilité trouvée pour la semaine précédente.'}, status=status.HTTP_404_NOT_FOUND)

        # Cloner les disponibilités en changeant seulement la semaine
        for dispo in anciennes_disponibilites:
            dispo.pk = None  # Crée un nouvel enregistrement
            dispo.semaine = semaine_actuelle
            dispo.save()

        return Response({'success': 'Disponibilités reconduites avec succès !'}, status=status.HTTP_201_CREATED)
    
class CalendrierViewSet(viewsets.ModelViewSet):
    queryset = Calendrier.objects.all()
    serializer_class = CalendrierSerializer

    def create(self, request, *args, **kwargs):
        """ Empêcher la création de doublons pour une même semaine/jour """
        semaine = request.data.get('semaine')
        jour = request.data.get('jour')

        if Calendrier.objects.filter(semaine=semaine, jour=jour).exists():
            return Response({'error': 'Un calendrier existe déjà pour ce jour.'}, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)

    def ajouter_exception(self, request):
        """ Ajouter une exception (jour férié ou événement académique) """
        semaine = request.data.get('semaine')
        jour = request.data.get('jour')
        creneaux_exceptionnels = request.data.get('creneaux_exceptionnels', [])

        try:
            calendrier = Calendrier.objects.get(semaine=semaine, jour=jour)
            calendrier.exception = True
            calendrier.creneaux_exceptionnels = creneaux_exceptionnels
            calendrier.save()
            return Response({'success': 'Exception ajoutée avec succès !'}, status=status.HTTP_200_OK)
        except Calendrier.DoesNotExist:
            return Response({'error': 'Calendrier introuvable.'}, status=status.HTTP_404_NOT_FOUND)

    def supprimer_jour(self, request):
        """ Supprimer une journée complète (jour férié) """
        semaine = request.data.get('semaine')
        jour = request.data.get('jour')

        try:
            calendrier = Calendrier.objects.get(semaine=semaine, jour=jour)
            calendrier.delete()
            return Response({'success': 'Journée supprimée avec succès !'}, status=status.HTTP_200_OK)
        except Calendrier.DoesNotExist:
            return Response({'error': 'Calendrier introuvable.'}, status=status.HTTP_404_NOT_FOUND)
        
        
        
class ChargeHebdomadaireViewSet(viewsets.ModelViewSet):
    queryset = ChargeHebdomadaire.objects.all()
    serializer_class = ChargeHebdomadaireSerializer

    
    def reconduire(self, request):
        """ Reconduire la configuration de la semaine précédente pour une matière """
        try:
            semaine_actuelle = request.data.get('semaine_actuelle')
            matiere_id = request.data.get('matiere')

            if not semaine_actuelle or not matiere_id:
                return Response({'error': 'Veuillez fournir la semaine actuelle et l\'ID de la matière.'}, status=status.HTTP_400_BAD_REQUEST)

            semaine_actuelle = datetime.strptime(semaine_actuelle, "%Y-%m-%d").date()
            semaine_precedente = semaine_actuelle - timedelta(days=7)

            charge_precedente = ChargeHebdomadaire.objects.filter(matiere=matiere_id, semaine=semaine_precedente).first()
            
            if not charge_precedente:
                return Response({'error': 'Aucune configuration trouvée pour la semaine précédente.'}, status=status.HTTP_404_NOT_FOUND)

            nouvelle_charge = ChargeHebdomadaire(
                matiere=charge_precedente.matiere,
                heures_cm=charge_precedente.heures_cm,
                heures_td=charge_precedente.heures_td,
                heures_tp=charge_precedente.heures_tp,
                semaine=semaine_actuelle,
                reconduction_de=charge_precedente
            )
            nouvelle_charge.save()

            return Response({'success': 'Configuration reconduite avec succès !'}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class AffectationEnseignantViewSet(viewsets.ModelViewSet):
    queryset = AffectationEnseignant.objects.all()
    serializer_class = AffectationEnseignantSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
class GroupeMatiereViewSet(viewsets.ModelViewSet):
    queryset = GroupeMatiere.objects.all()
    serializer_class = GroupeMatiereSerializer

class EmploiTempsViewSet(viewsets.ModelViewSet):
    queryset = EmploiTemps.objects.all()
    serializer_class = EmploiTempsSerializer
    
    
class ContrainteHoraireViewSet(viewsets.ModelViewSet):
    queryset = ContrainteHoraire.objects.all()
    serializer_class = ContrainteHoraireSerializer

@api_view(['GET'])
def get_enseignant_disponibilites(request, enseignant_id):
    try:
        enseignant = Enseignant.objects.get(id=enseignant_id)
        disponibilites = enseignant.get_disponibilites()
        return Response({"enseignant": enseignant.nom, "disponibilites": disponibilites}, status=status.HTTP_200_OK)
    except Enseignant.DoesNotExist:
        return Response({"error": "Enseignant non trouvé"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_groupe_matiere(request, groupe_id):
    try:
        groupe = Groupe.objects.get(id=groupe_id)
        matieres = groupe.get_matieres()
        return Response({"groupe": groupe.nom, "matieres": matieres}, status=status.HTTP_200_OK)
    except Groupe.DoesNotExist:
        return Response({"error": "Groupe non trouvé"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_matiere_enseignants(request, matiere_id):
    try:
        matiere = Matiere.objects.get(id=matiere_id)
        enseignants = matiere.get_enseignants()
        return Response({"matiere": matiere.nom, "enseignants": enseignants}, status=status.HTTP_200_OK)
    except Matiere.DoesNotExist:
        return Response({"error": "Matière non trouvée"}, status=status.HTTP_404_NOT_FOUND)


from django.db import transaction
from rest_framework import viewsets
from datetime import timedelta ,date
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Matiere, Enseignant ,Groupe ,Calendrier ,AffectationEnseignant ,GroupeMatiere ,ContrainteHoraire ,Disponibilite ,ChargeHebdomadaire ,EmploiTemps,Salle
from .serializers import MatiereSerializer, EnseignantSerializer ,GroupeSerializer,CalendrierSerializer ,DisponibiliteSerializer,AffectationEnseignantSerializer,SalleSerializer,GroupeMatiereSerializer,ChargeHebdomadaireSerializer ,ContrainteHoraireSerializer,EmploiTempsSerializer
from .services import generer_emploi_temps

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
        disponibilites = request.data  
        
        if not isinstance(disponibilites, list):
            return Response({'error': 'Les données doivent être une liste.'}, status=status.HTTP_400_BAD_REQUEST)

        nouvelles_disponibilites = []
        erreurs = []

        try:
            with transaction.atomic(): 
                for dispo_data in disponibilites:
                    enseignant = dispo_data.get('enseignant')
                    jour = dispo_data.get('jour')
                    creneau = dispo_data.get('creneau')
                    semaine = dispo_data.get('semaine')

                    if Disponibilite.objects.filter(
                        enseignant=enseignant, jour=jour, creneau=creneau, semaine=semaine
                    ).exists():
                        erreurs.append({
                            'enseignant': enseignant,
                            'jour': jour,
                            'creneau': creneau,
                            'semaine': semaine,
                            'error': 'Cet enseignant est déjà disponible sur ce créneau.'
                        })
                        continue

                    serializer = self.get_serializer(data=dispo_data)
                    serializer.is_valid(raise_exception=True)
                    nouvelles_disponibilites.append(serializer.save())

                if erreurs:
                    raise ValueError("Certaines disponibilités sont en conflit.")

        except ValueError:
            return Response({'error': 'Une ou plusieurs disponibilités existent déjà.', 'details': erreurs},status=status.HTTP_400_BAD_REQUEST)

        return Response({'success': 'Disponibilités enregistrées avec succès !'}, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        disponibilites = request.data  
        
        if not isinstance(disponibilites, list):
            return Response({'error': 'Les données doivent être une liste.'}, status=status.HTTP_400_BAD_REQUEST)

        mises_a_jour = []
        erreurs = []

        try:
            with transaction.atomic():  
                for dispo_data in disponibilites:
                    dispo_id = dispo_data.get('id')
                    enseignant = dispo_data.get('enseignant')
                    jour = dispo_data.get('jour')
                    creneau = dispo_data.get('creneau')
                    semaine = dispo_data.get('semaine')

                    try:
                        dispo_instance = Disponibilite.objects.get(id=dispo_id)
                        
                        if Disponibilite.objects.filter(
                            enseignant=enseignant, jour=jour, creneau=creneau, semaine=semaine
                        ).exclude(id=dispo_id).exists():
                            erreurs.append({
                                'id': dispo_id,
                                'enseignant': enseignant,
                                'jour': jour,
                                'creneau': creneau,
                                'semaine': semaine,
                                'error': 'Ce créneau est déjà occupé par cet enseignant.'
                            })
                            continue 

                        serializer = self.get_serializer(dispo_instance, data=dispo_data, partial=True)
                        serializer.is_valid(raise_exception=True)
                        mises_a_jour.append(serializer.save())

                    except Disponibilite.DoesNotExist:
                        erreurs.append({'id': dispo_id, 'error': 'Disponibilité introuvable.'})

                if erreurs:
                    raise ValueError("Certaines mises à jour sont en conflit.")

        except ValueError:
            return Response({'error': 'Une ou plusieurs mises à jour ont échoué.', 'details': erreurs},status=status.HTTP_400_BAD_REQUEST)

        return Response({'success': 'Disponibilités mises à jour avec succès !'}, status=status.HTTP_200_OK)
    
    def reconduire_disponibilites(self, request):
        semaine_actuelle = request.data.get('semaine_actuelle')
        semaine_precedente = semaine_actuelle - timedelta(days=7)
        enseignant_id = request.data.get('enseignant')

        anciennes_disponibilites = Disponibilite.objects.filter(enseignant=enseignant_id, semaine=semaine_precedente)
        if not anciennes_disponibilites.exists():
            return Response({'error': 'Aucune disponibilité trouvée pour la semaine précédente.'}, status=status.HTTP_404_NOT_FOUND)

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

  
class SalleViewSet(viewsets.ModelViewSet):
    queryset = Salle.objects.all()
    serializer_class = SalleSerializer  
    
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


class EmploiTempsGroupeViewSet(viewsets.ViewSet):
    def list(self, request, groupe_id, semaine):
        emplois = EmploiTemps.objects.filter(groupe_id=groupe_id, semaine=semaine)
        serializer = EmploiTempsSerializer(emplois, many=True)
        return Response(serializer.data)

class EmploiTempsEnseignantViewSet(viewsets.ViewSet):
    def list(self, request, enseignant_id, semaine):
        emplois = EmploiTemps.objects.filter(enseignant_id=enseignant_id, semaine=semaine)
        serializer = EmploiTempsSerializer(emplois, many=True)
        return Response(serializer.data)

# Viewset pour générer ou mettre à jour l'emploi du temps actuel
class GenererEmploiTempsViewSet(viewsets.ViewSet):
    def create(self, request):
        semaine_actuelle = date.today() - timedelta(days=date.today().weekday())
        message = generer_emploi_temps(semaine_actuelle)
        return Response({"message": message})


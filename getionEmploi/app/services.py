from ortools.linear_solver import pywraplp
from django.db.models import Q
from .models import (
    Enseignant, Matiere, Groupe, Salle, Disponibilite, ChargeHebdomadaire,
    AffectationEnseignant, EmploiTemps, ContrainteHoraire
)
from datetime import date, timedelta
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import EmploiTempsSerializer

# Générer ou mettre à jour l'emploi du temps
def generer_emploi_temps(semaine):
    solver = pywraplp.Solver.CreateSolver('CBC')
    
    groupes = list(Groupe.objects.all())
    matieres = list(Matiere.objects.all())
    enseignants = list(Enseignant.objects.all())
    salles = list(Salle.objects.all())
    affectations = list(AffectationEnseignant.objects.all())
    contraintes = list(ContrainteHoraire.objects.all())
    charges = list(ChargeHebdomadaire.objects.filter(semaine=semaine))
    disponibilites = list(Disponibilite.objects.filter(semaine=semaine))
    
    G = len(groupes)
    J = len(matieres)
    I = len(enseignants)
    K = 25  # Nombre de créneaux disponibles
    S = len(salles)
    STP = len([s for s in salles if s.type_salle == 'TP'])
    
    # Construction de la liste des conflits entre groupes (chevauchements)
    conflits = []
    for g1 in range(G):
        for g2 in range(G):
            if g1 < g2 and (groupes[g1].parent == groupes[g2] or groupes[g2].parent == groupes[g1]):
                conflits.append((g1, g2))
    
    # Variables de décision
    X = [[[solver.IntVar(0, 1, f'X_{g}_{j}_{k}') for k in range(K)] for j in range(J)] for g in range(G)]
    Y = [[[solver.IntVar(0, 1, f'Y_{g}_{j}_{k}') for k in range(K)] for j in range(J)] for g in range(G)]
    Z = [[[solver.IntVar(0, 1, f'Z_{g}_{j}_{k}') for k in range(K)] for j in range(J)] for g in range(G)]
    
    # Résolution du modèle
    status = solver.Solve()
    
    if status == pywraplp.Solver.OPTIMAL:
        for g in range(G):
            for j in range(J):
                for k in range(K):
                    if X[g][j][k].solution_value() > 0 or Y[g][j][k].solution_value() > 0 or Z[g][j][k].solution_value() > 0:
                        emploi, created = EmploiTemps.objects.update_or_create(
                            groupe=groupes[g],
                            matiere=matieres[j],
                            enseignant=AffectationEnseignant.objects.get(
                                groupe=groupes[g], matiere=matieres[j]
                            ).enseignant,
                            semaine=semaine,
                            defaults={
                                "semestre": groupes[g].semestre,
                                "jour": ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi'][k // 5],
                                "creneau": f'P{k % 5 + 1}',
                                "type_cours": 'CM' if X[g][j][k].solution_value() > 0 else ('TP' if Y[g][j][k].solution_value() > 0 else 'TD')
                            }
                        )
    
    return f"Emploi du temps pour la semaine {semaine} généré avec succès !"


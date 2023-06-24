"""
  Fichier dedie au programme mathematique en une seule dimension
"""

import gurobipy as gp

import methodeVote


def methodeLineaire(nbcandidats, nborders, tabOrders, temps):
    """Fonction de calcul des coordinées par le programme mathématique linéaire"""

    dimension = 1

    # Model gurobi
    model = gp.Model('Repartition')

    # pour resoudre des equations quadratiques
    model.params.NonConvex = 2
    model.update()

    # Variables : coordonnees des candidats / votants + distances

    # Tableau a 1 dimension de taille nbCandidats
    coordonneescandidats = model.addVars(nbcandidats,
                                         dimension,
                                         name="coordonneescandidats")

    # Tableau a 1 dimension de taille nbVotants
    coordonneesvotants = model.addVars(nborders,
                                       dimension,
                                       name="coordonneesvotants")

    distances = model.addVars(nborders, nbcandidats, name="distances")

    # Calcul des distances
    for v in range(nborders):
        pref = tabOrders[v]
        tab = methodeVote.prefComplete(pref)

        for c in range(len(tab)):
            distances[v, tab[c] - 1] = (coordonneescandidats[tab[c] - 1, 0] -
                                        coordonneesvotants[v, 0])**2

    # Ajout des variables sigma

    LV = methodeVote.creationLV(tabOrders, nborders)
    nbCouples = methodeVote.sommeLV(LV)
    sigmas = model.addVars(nborders, nbCouples, name="sigmas")
    model.update()

    # Ajout des contraintes sur les valeurs des coordonnees; ainsi que sur les distances

    C = {i for i in range(nbcandidats)}
    V = {i for i in range(nborders)}

    model.addConstrs((coordonneescandidats[i, 0] >= 0 for i in C),
                     name="min 0")
    model.addConstrs((coordonneescandidats[i, 0] <= 1 for i in C),
                     name="max 1")

    model.addConstrs((coordonneesvotants[i, 0] >= 0 for i in V), name="min 0")
    model.addConstrs((coordonneesvotants[i, 0] <= 1 for i in V), name="max 1")

    model.addConstrs((distances[v, c] >= 0 for c in C for v in V),
                     name="distance")

    # Contraintes sur les sigmas

    model.addConstrs((sigmas[v, LV[v].index((c1, c2))] >= 0 for v in V
                      for (c1, c2) in LV[v]),
                     name="sigmas_positifs_ou_nuls")
    model.update()

    model.addConstrs((sigmas[v, LV[v].index(
        (c1, c2))] + distances[v, c2 - 1] >= distances[v, c1 - 1] + 10**(-3)
                      for v in V for (c1, c2) in LV[v]),
                     name="sigma")
    model.update()

    # Fonction a minimiser : on va tenir compte du nombre de votants
    # Remarque : nb_Voters_choix est une ponderation
    model.setObjective((gp.quicksum(
        gp.quicksum(tabOrders[v][0] * sigmas[v, LV[v].index((c1, c2))]
                    for (c1, c2) in LV[v]) for v in V)), gp.GRB.MINIMIZE)
    model.update()

    model.Params.MIPGap = 0.05  # 5%
    model.Params.TimeLimit = temps  # temps en secondes donne en parametre
    model.optimize()

    # Cle en format : [i,j] avec i = identifiant du candidat et j = 0 ou 1 (la coordonee X ou Y)
    candidats = {k: v.X for k, v in coordonneescandidats.items()}

    # Cle en format : [i,j] avec i = identifiant de la preference et j = 0 ou 1 (la coordonee X ou Y)
    votants = {k: v.X for k, v in coordonneesvotants.items()}

    # On recupere le modele en format fichier mps
    model.write('model.mps')

    return candidats, votants

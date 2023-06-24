"""
  Fichier dedie au programme mathematique en deux dimensions pour des donnees de vote
"""

import gurobipy as gp

# Modification pour creer moins de contraintes pour des preferences incompletes


def creationLV(tabOrders, nborders):
    """Creation d'un dictionnaire LV qui contient les paires (c,c') telles que c > c'"""

    # les cles sont des entiers de 0 à nbOrders-1

    LV = dict()
    for i in range(nborders):
        pref = prefComplete(tabOrders[i])

        LV[i] = [(pref[j], pref[k]) for j in range(len(pref))
                 for k in range(j + 1, len(pref))]
    return LV


def sommeLV(lv):
    """Renvoie le nombre total de couples possibles"""
    res = 0
    for liste in lv.values():
        res = res + len(liste)
    return res


def prefComplete(pref):
    """Fonction qui retourne la preference sans les -1"""
    cpt = 0
    for i in range(1, len(pref)):
        if (pref[i] != -1):
            cpt = cpt + 1
    return pref[1:(cpt + 1)]


def methodeSigma(nbcandidats, nborders, tabOrders, temps):

    dimension = 2

    # Model gurobi
    model = gp.Model('Repartition')

    # Pour resoudre des equations quadratiques
    model.params.NonConvex = 2
    model.update()

    # Variables : coordonnees des candidats / votants + distances

    # Tableau a 2 dimension de taille nbCandidats
    coordonneescandidats = model.addVars(nbcandidats,
                                         dimension,
                                         name="coordonneescandidats")

    # Tableau a 2 dimension de taille nbVotants
    coordonneesvotants = model.addVars(nborders,
                                       dimension,
                                       name="coordonneesvotants")

    distances = model.addVars(nborders, nbcandidats, name="distances")
    # Calcul des distances euclidiennes
    for v in range(nborders):
        pref = tabOrders[v]
        tab = prefComplete(pref)
        for c in range(len(tab)):
            distances[v, tab[c]] = ((coordonneescandidats[tab[c] - 1, 0] -
                                     coordonneesvotants[v, 0])**2 +
                                    (coordonneescandidats[tab[c] - 1, 1] -
                                     coordonneesvotants[v, 1])**2)

    # Dictionnaire des paires
    LV = creationLV(tabOrders, nborders)
    nbCouples = sommeLV(LV)

    sigmas = model.addVars(nborders, nbCouples, name="sigmas")
    model.update()

    # Ajout des contraintes sur les valeurs des coordonnees; ainsi que sur les distances

    C = {i for i in range(nbcandidats)}
    V = {i for i in range(nborders)}

    model.addConstrs((coordonneescandidats[i, 0] >= 0 for i in C),
                     name="min 0")
    model.addConstrs((coordonneescandidats[i, 1] >= 0 for i in C),
                     name="min 0")
    model.addConstrs((coordonneescandidats[i, 0] <= 1 for i in C),
                     name="max 1")
    model.addConstrs((coordonneescandidats[i, 1] <= 1 for i in C),
                     name="max 1")

    model.addConstrs((coordonneesvotants[i, 0] >= 0 for i in V), name="min 0")
    model.addConstrs((coordonneesvotants[i, 1] >= 0 for i in V), name="min 0")
    model.addConstrs((coordonneesvotants[i, 0] <= 1 for i in V), name="max 1")
    model.addConstrs((coordonneesvotants[i, 1] <= 1 for i in V), name="max 1")

    for v in range(nborders):
        pref = tabOrders[v]
        tab = prefComplete(pref)
        model.addConstrs(
            (distances[v, tab[c] - 1] >= 0 for c in range(len(tab))),
            name="distance")
    model.update()

    # Contraintes sur les sigmas
    model.addConstrs((sigmas[v, LV[v].index(
        (c1, c2))] + distances[v, c1 - 1] >= distances[v, c2 - 1] + 10**(-5)
                      for v in V for (c1, c2) in LV[v]),
                     name="sigma")
    model.update()

    # Fonction a minimiser : on va tenir compte du nb de votants pour une la fonction a minimiser
    # nb_Voters_choix c'est une ponderation
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

    return candidats, votants

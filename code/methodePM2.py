"""
  Fichier dedie au programme mathematique en deux dimensions
"""

import gurobipy as gp


def creationLV(tabOrders, nborders, nbcandidats):
    """Créé un dictionnaire LV qui contient les paires (c,c') telles que c > c'"""

    # Les cles sont des entiers de 0 à nbOrders-1

    LV = dict()
    for i in range(nborders):
        LV[i] = [(tabOrders[i][j], tabOrders[i][k])
                 for j in range(1, nbcandidats + 1)
                 for k in range(j + 1, nbcandidats + 1)]

    return LV


def methodeSigma(nbcandidats, nborders, tabOrders, temps):
    """Fonction de calcul des coordinées par le programme mathématique en 2D"""
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
    for c in range(nbcandidats):
        for v in range(nborders):
            distances[v, c] = (
                (coordonneescandidats[c, 0] - coordonneesvotants[v, 0])**2 +
                (coordonneescandidats[c, 1] - coordonneesvotants[v, 1])**2)

    sigmas = model.addVars(nborders, (nbcandidats * (nbcandidats - 1) // 2),
                           name="sigmas")
    model.update()

    # Dictionnaire des paires
    LV = creationLV(tabOrders, nborders, nbcandidats)

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

    model.addConstrs((distances[v, c] >= 0 for c in C for v in V),
                     name="distance")
    model.update()

    # Contraintes sur les sigmas
    model.addConstrs((sigmas[v, LV[v].index((c1, c2))] >= 0 for v in V
                      for (c1, c2) in LV[v]),
                     name="sigmas_positifs_ou_nuls")
    model.update()
    model.addConstrs((sigmas[v, LV[v].index(
        (c1, c2))] + distances[v, c2 - 1] >= distances[v, c1 - 1] + 10**(-5)
                      for v in V for (c1, c2) in LV[v]),
                     name="sigma")
    model.update()

    # Fonction a minimiser : on va tenir compte du nb de votants pour une la fonction a minimiser
    # Remarque : nb_Voters_choix est une ponderation
    model.setObjective((gp.quicksum(
        gp.quicksum(tabOrders[v][0] * sigmas[v, LV[v].index((c1, c2))]
                    for (c1, c2) in LV[v]) for v in V)), gp.GRB.MINIMIZE)
    model.update()

    model.Params.MIPGap = 0.05  # 5%
    model.Params.TimeLimit = temps  # temps en secondes donne en parametre
    model.optimize()

    #Cle en format : [i,j] avec i = identifiant du candidat et j = 0 ou 1 (la coordonee X ou Y)
    candidats = {k: v.X for k, v in coordonneescandidats.items()}
    #Cle en format : [i,j] avec i = identifiant de la preference et j = 0 ou 1 (la coordonee X ou Y)
    votants = {k: v.X for k, v in coordonneesvotants.items()}

    # On recupere le modele en format fichier mps
    model.write('model.mps')

    return candidats, votants

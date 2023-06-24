"""
  Fichier dedie aux fonctions d'evaluation des resultats
"""


def insertionElem(tab, j):
    """Fonction utilisée dans le tri par insertion"""
    tmp = tab[j]
    i = j - 1

    while i > -1 and tab[i][1] > tmp[1]:
        tab[i + 1] = tab[i]
        i = i - 1
        tab[i + 1] = tmp


def tri(liste):
    """Fonction de tri par insertion d'une liste - ordre decroissant"""
    j = 1
    n = len(liste)
    while j != n:
        insertionElem(liste, j)
        j = j + 1


# renommer a completerPref
def modifiePref(prefInitial, prefFinal, nbcandidats):
    """Modifie une préference si elle est incomplète en rajoutant les alternatives non classées à la fin du tableau"""

    #liste des candidats classés pour une préference initiale donnée
    candidatsClasses = [i for i in prefInitial if i != -1]
    #liste des candidats non classés pour cette préference
    candidatsNonClasses = [
        i for i in range(1, nbcandidats + 1) if i not in prefInitial
    ]

    #préférence initiale complétée
    resInit = candidatsClasses + candidatsNonClasses

    #préférence finale complétée
    resFinal = [i for i in prefFinal if i in prefInitial if i != -1]
    resFinal = resFinal + candidatsNonClasses

    return resInit, resFinal


def recalcule_pref(candidats, votants, nbcandidats, nborders, dimension):
    """Fonction qui créer le tabOrders de la représentation obtenue comme résultat par les programmes mathématiques"""

    tabRepr = []

    for v in range(nborders):
        listePref = []
        for c in range(nbcandidats):

            #calculer les distances
            distance = (candidats[(c, 0)] - votants[(v, 0)])**2
            if dimension == 2:
                distance += (candidats[(c, 1)] - votants[(v, 1)])**2
            listePref.append([c + 1, distance])

        tri(listePref)

        prefV = [listePref[i][0] for i in range(len(listePref))]
        tabRepr.append(prefV)

    return tabRepr


def evaluer(candidats, votants, nbcandidats, nborders, tabOrders, dimension):
    """Fonction qui donne le tau de Kendall de la représentation : 
  l'accord parfait donne 0 et le désaccord complet donne 1"""

    # Ces tableaux sont des matrices
    tabRepresentation = recalcule_pref(candidats, votants, nbcandidats,
                                       nborders, dimension)
    tabInitial = [tabOrders[i][1:] for i in range(len(tabOrders))]
    nbVoters = sum(tabOrders[i][0] for i in range(len(tabOrders)))

    tabOrderI = []
    tabOrderF = []

    # On complete les preferences incompletes
    for i in range(nborders):
        prefI, prefF = modifiePref(tabInitial[i], tabRepresentation[i],
                                   nbcandidats)
        tabOrderI.append(prefI)
        tabOrderF.append(prefF)

    # On calcule le tau
    tau = 0

    # Pour chaque preference ie. chaque votant
    for k in range(len(tabOrderI)):
        # On compare l'ordre dans la liste initiale (pour une preference)
        # avec l'ordre obtenu dans la liste donnée par le programme :

        # Parcours du tableau initial
        for i in range(0, len(tabOrderI[k])):
            for j in range(i + 1, len(tabOrderI[k])):
                # On recupere l'indice dans le tableau final
                indice = tabOrderF[k].index(tabOrderI[k][j])
                # Comparaison de l'ordre
                if tabOrderI[k][i] in tabOrderF[k][indice + 1:]:
                    #ponderation
                    tau += tabOrders[k][0]

    tau = (2 * tau) / (nbcandidats * (nbcandidats - 1) * nbVoters)

    return tau


def NMDStoDict(scaled_df, dimension, nbcandidats, tabOrders):
    """Fonction qui donne le dictionnaire qui représente les résultats obtenus par la méthode NMDS
    Remarque : on compte chaque préférence qu'une seule fois"""

    # Dictionnaires des coordonnées
    candidats = dict()
    votants = dict()

    # Construction du dictionnaire candidats
    for i in range(nbcandidats):
        if dimension == 1:
            candidats.update({(i, 0): scaled_df[i]})
        elif dimension == 2:
            candidats.update({(i, 0): scaled_df[i][0]})
            candidats.update({(i, 1): scaled_df[i][1]})

    # Constuction du dictionnaire votants

    if dimension == 1:
        votants.update({(0, 0): scaled_df[nbcandidats]})
    elif dimension == 2:
        votants.update({(0, 0): scaled_df[nbcandidats][0]})
        votants.update({(0, 1): scaled_df[nbcandidats][1]})

    j = nbcandidats
    index = 0
    while j < len(scaled_df):
        if dimension == 1:
            votants.update({(index, 0): scaled_df[j]})
        elif dimension == 2:
            votants.update({(index, 0): scaled_df[j][0]})
            votants.update({(index, 1): scaled_df[j][1]})
        j += tabOrders[index][0]
        index += 1

    return candidats, votants

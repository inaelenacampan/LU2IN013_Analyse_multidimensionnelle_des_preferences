"""
  Fichier dedie a la lecture des donnees des fichiers .csv (application aux donnees de vote)
  Source : Projet VoterAutrement
"""

import pandas as pd
import math
import numpy as np


def estVide(tab, i, j):
    """Renvoie true si la case (i, j) de tab est vide, false sinon"""
    return math.isnan(tab.iloc[i][j])


def chercheScore(tab, score):
    """Renvoie l'indide de la valuer score dans tab, et -1 sinon"""
    for i in range(len(tab)):
        if tab[i] == score:
            return i
    return -1


def read_file(path):
    """Lit le fichier path"""
    # On lit le tableau
    tab = pd.read_csv(path)
    candidats = tab.columns[1:len(tab.columns) - 1]

    tabOrders = []

    # On met les score des candidats dans un tableau
    for i in range(1, len(tab)):
        tab_score = np.zeros(len(candidats), dtype=int)
        for j in range(1, len(candidats) + 1):
            if not estVide(tab, i, j):
                tab_score[j - 1] = tab.iloc[i][j]
            else:
                # Si le votant n'a pas mis ce candidats dans la preference, on le met a 0
                tab_score[j - 1] = 0

        # On met dans un tab les préférences
        preference = []

        for score in range(11, 1, -1):
            index = chercheScore(tab_score, score)
            if index != -1:
                preference.append(index + 1)
            else:
                # Si le votant n'a pas mis ce candidats dans la preference, on le met a -1
                preference.append(-1)

        tabOrders.append(preference)

    # pour tabOrders, on peut appeler la fonction modifTabOrders pour renvoyer directement ce qu'on veut
    tabOrders = modifTabOrders(tabOrders)
    if (len(tabOrders) > 400):
        return candidats, len(candidats), len(tab) - 1, 400, tabOrders[0:400]

    return candidats, len(candidats), len(tab) - 1, len(tabOrders), tabOrders


def estDans(tab, preference):
    """Fonction qui compare les preferences 
    on ne prend pas en compte la premiere case car c'est le nonmbre de votants qui ont cette preference"""

    for pref in tab:
        if pref[1:] == preference[1:]:
            return True
    return False


def chercheIndicePref(tabOrders, preference):
    """Fonction qui renvoie l'indice de la preference dans tabOrders"""

    for i in range(len(tabOrders)):
        if tabOrders[i][1:] == preference[1:]:
            return i


def insertionElem(tab, j):
    """Fonction utilisée dans le tri par insertion"""

    tmp = tab[j]
    i = j - 1
    while i > -1 and tab[i][0] < tmp[0]:
        tab[i + 1] = tab[i]
        i = i - 1
        tab[i + 1] = tmp


def tri(liste):
    """Fonction de tri par insertion"""

    j = 1
    n = len(liste)
    while j != n:
        insertionElem(liste, j)
        j = j + 1


def modifTabOrders(orders):
    """Fonction qui modifie orders pour mettre le nombre de votants pour chaque preferences et qui la trie en fonction de ce nombre"""
    tabOrders = []

    for pref in orders:
        # on rajoute la premiere case pour le nb de votants qui ont cette préférence
        newPref = [1]
        for cand in pref:
            newPref.append(cand)

        # Si la preference est deja dans tabOrders, on incremente le nb de votants
        if estDans(tabOrders, newPref):
            index = chercheIndicePref(tabOrders, newPref)
            tabOrders[index][0] = tabOrders[index][0] + 1

        # Sinon, on ajoute la preference
        else:
            tabOrders.append(newPref)

    tri(tabOrders)
    return tabOrders

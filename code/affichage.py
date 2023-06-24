"""
  Fichier dedie aux fonctions d'affichage du menu et des graphes des solutions
"""

import matplotlib.pyplot as plt
import numpy as np


def menu_methode():
    """Affichage des méthodes disponibles"""

    print("------------MENU----------------\n")

    print('q : Quitter\n')
    print('1 : Programmation mathematique en 2 dimensions\n')
    print('2 : Programmation mathematique en une seule dimension\n')
    print('3 : Methode NMDS en 2 dimensions\n')
    print('4 : Methode NMDS en une seule dimension\n')
    print('5 : Analyse des methodes en dimension 2\n')
    print('c : Changer de fichier\n')

    print("--------------------------------\n")

    res = input('Choix de methode = ')

    if res == 'q' or res == 'c' or res == '3' or res == '4':
        # les methodes NMDS ne prennent pas une variable temps en parametre
        return res, 0

    # ajout la demande du temps max de calcul
    temps = int(input('Temps max d execution (en secondes) = '))
    return res, temps


def evaluation():
    """Demande si on effectue l'évaluation de la methode"""

    res = input('\nVoulez vous evaluer la methode ? o/n\n')
    return res


def affichagAvecVotants():
    """Demande à l'utilisatuer affiche aussi les votants"""

    res = input('\nVoulez vous afficher aussi les votants ? o/n\n')
    return res


def affichage_candidatsPM2(nbCandidats, Dict, nomCandidats):
    """Affichage des candidats dans un plan en programmation mathematiques en dimension 2"""

    for i in range(nbCandidats):
        plt.scatter(Dict[(i, 0)], Dict[(i, 1)], color='red', s = 8)
        plt.annotate(
            text=nomCandidats[i],  # nom du candidat
            xy=(Dict[(i, 0)], Dict[(i, 1)]),  # les coordonnees du candidat
            xytext=(Dict[(i, 0)], Dict[(i, 1)] - 0.03))


def affichage_votantsPM2(nbOrders, Dict, nbVotants):
    """Affichage des votants dans un plan en prommation mathematiques en dimension 2"""

    for i in range(nbOrders):
        plt.scatter(Dict[(i, 0)],
                    Dict[(i, 1)],
                    s=nbVotants[i][0]*5,
                    color='blue')


def affichage_candidatsPM1(nbCandidats, Dict, nomCandidats):
    """Affichage des candidats dans un plan en programmation mathematiques en dimension 1"""

    for i in range(nbCandidats):
        plt.scatter(Dict[(i, 0)], 0, s=1, color='red')
        plt.annotate(text=nomCandidats[i],
                     xy=(Dict[(i, 0)], 0),
                     xytext=(Dict[(i, 0)], 0.03))


def affichage_votantsPM1(nbOrders, Dict, nbVotants):
    """Affichage des votants dans un plan en programmation mathematiques en dimension 1"""

    for i in range(nbOrders):
        plt.scatter(Dict[(i, 0)], 0, color='blue')


def affichage_presidentielle(nbCandidats, Dict, Candidats):
    """Affichage des candidats des elections presidentielles dans un plan"""

    colors = [
        'red', 'black', 'blue', 'green', 'gray', 'pink', 'magenta', 'yellow',
        'cyan', 'brown', 'orange'
    ]

    candidats = [
        'NA', 'FA', 'JC', 'NDA', 'FF', 'BH', 'JL', 'MLP', 'EM', 'JLM', 'PP'
    ]

    j = 0.03
    for i in range(nbCandidats):
        print(colors[i] + ' : ' + Candidats[i])
        plt.scatter(Dict[(i, 0)], 0, s=1, color=colors[i], label=Candidats[i])
        plt.annotate(
            text=candidats[i],
            xy=(Dict[(i, 0)], 0),
            xytext=(Dict[(i, 0)], j),  # position du texte
            arrowprops=dict(facecolor='black',
                            arrowstyle="-",
                            connectionstyle="bar,angle=180,fraction=-0.2")
        )  #la fleche vers le nom du candidat

        if i % 2 == 0:
            j = j * (-1)
        else:
            j = j - 0.005

    plt.legend()


def affichageNMDS2(scaled_df, nbcandidats, nborders, avecVotants, nomCandidats,
                   tabOrders):
    """Affichage des candidats et votants dans un plan par le NMDS en dimension 2"""

    #if (avecVotants == 1):
    #    plt.scatter(scaled_df[:, 0], scaled_df[:, 1])
    #else:
    #    plt.scatter(scaled_df[:nbcandidats, 0], scaled_df[:nbcandidats, 1])

    # nom des axes

    plt.xlabel('Coordinate 1')
    plt.ylabel('Coordinate 2')

    # ajouter un nom a chaque point
    for i in range(nbcandidats):
        plt.scatter(scaled_df[:, 0][i], scaled_df[:, 1][i])
        plt.annotate(nomCandidats[i],
                     (scaled_df[:, 0][i] + .01, scaled_df[:, 1][i]),
                     color='red',
                     rotation=60)

    if avecVotants == 1:
        index = 0
        i = nbcandidats
        while i < len(scaled_df):
            plt.scatter(scaled_df[:, 0][i],
                        scaled_df[:, 1][i],
                        s=tabOrders[index][0],
                        color='blue')
            plt.annotate('V' + str(index + 1),
                         (scaled_df[:, 0][i] + .02, scaled_df[:, 1][i]),
                         color='brown')
            i += tabOrders[index][0]
            index += 1


def affichageNMDS1(scaled_df, nbcandidats, nborders, avecVotants, nomCandidats,
                   tabOrders):
    """Affichage des candidats et votants dans un plan par le NMDS en dimension 1"""

    # matrice avce que des zeros (pour les ordonnées)
    Oy = np.zeros(len(scaled_df))

    # ajoute les points

    #if (avecVotants == 1):
    #    plt.scatter(scaled_df, Oy)
    #else:
    #    plt.scatter(scaled_df[:nbcandidats, 0], Oy[:nbcandidats])

    # ajoute les noms aux points
    for i in range(nbcandidats):
        plt.scatter(scaled_df[:, 0][i], Oy[i])
        plt.annotate(nomCandidats[i], (scaled_df[i] + .01, Oy[i]),
                     color='red',
                     rotation=60)

    if (avecVotants == 1):
        index = 0
        i = nbcandidats
        while i < len(scaled_df):
            plt.scatter(scaled_df[:, 0][i],
                        Oy[i],
                        s=tabOrders[index][0],
                        color='blue')
            plt.annotate('V' + str(index + 1), (scaled_df[i] + .02, Oy[i]),
                         color='brown')
            i += tabOrders[index][0]
            index += 1

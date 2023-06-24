"""
  Fichier principal (interface) pour lancer des tests
"""

import lecture
import lectureVote
import methodePM1
import methodePM2
import methodeVote
import methodeNMDS1
import methodeNMDS2
import affichage
import evaluation
import graph

import time
import matplotlib.pyplot as plt

# Recuperation du nom du fichier
print('Nom du fichier : ')
path = input()

# Lecture dediee selon l'extension
# Le fichier est un .soc
if (path[-4:] == '.soc'):
    path = 'soc/' + path
    nbcandidats, nbvoters, nborders, tabOrders, nomCandidats = lecture.read_file(
        path)

# Le fichier est un .csv
elif (path[-4:] == '.csv'):
    nomCandidats, nbcandidats, nbvoters, nborders, tabOrders = lectureVote.read_file(
        path)

choix, temps = affichage.menu_methode()

while choix != 'q':

    # Changement du fichier a analyser
    if choix == 'c':
        print('Nom du fichier : ')
        path = input()

        if (path[-4:] == '.soc'):
            path = 'soc/' + path
            nbcandidats, nbvoters, nborders, tabOrders, nomCandidats = lecture.read_file(
                path)

        elif (path[-4:] == '.csv'):
            nomCandidats, nbcandidats, nbvoters, nborders, tabOrders = lectureVote.read_file(
                path)

        choix, temps = affichage.menu_methode()

    # Methode : programmation mathematiques en dimension 2
    if choix == '1':

        if (path[-4:] == '.soc'):
            candidats, votants = methodePM2.methodeSigma(
                nbcandidats, nborders, tabOrders, temps)

        elif (path[-4:] == '.csv'):
            candidats, votants = methodeVote.methodeSigma(
                nbcandidats, nborders, tabOrders, temps)

        # affichage
        affichage.affichage_candidatsPM2(nbcandidats, candidats, nomCandidats)

        afficheVotant = affichage.affichagAvecVotants()
        if afficheVotant == 'o':
            affichage.affichage_votantsPM2(nborders, votants, tabOrders)

        plt.show()

        # evaluation
        eval = affichage.evaluation()

        if eval == 'o':
            time.sleep(0.75)
            tau = evaluation.evaluer(candidats, votants, nbcandidats, nborders,
                                     tabOrders, 2)
            print('tau = ' + str(tau))
            time.sleep(0.75)

    # Methode : programmation mathématique en dimension 1
    if choix == '2':

        candidats, votants = methodePM1.methodeLineaire(
            nbcandidats, nborders, tabOrders, temps)

        # affichage
        if (path[-4:] == '.soc'):
            affichage.affichage_candidatsPM1(nbcandidats, candidats,
                                             nomCandidats)

            afficheVotant = affichage.affichagAvecVotants()
            if afficheVotant == 'o':
                affichage.affichage_votantsPM1(nborders, votants, nbvoters)

        elif (path[-4:] == '.csv'):
            affichage.affichage_presidentielle(nbcandidats, candidats,
                                               nomCandidats)

        plt.show()

        # evaluation
        eval = affichage.evaluation()

        if eval == 'o':
            time.sleep(0.75)
            tau = evaluation.evaluer(candidats, votants, nbcandidats, nborders,
                                     tabOrders, 1)
            print('tau = ' + str(tau))
            time.sleep(0.75)

    # Methode : NMDS en dimension 2
    if choix == '3':

        scaled_df = methodeNMDS2.methodeNMDS2(nbcandidats, tabOrders)

        # affichage
        afficheVotant = affichage.affichagAvecVotants()
        avecVotant = 0
        if afficheVotant == 'o':
            avecVotant = 1

        if (path[-4:] == '.soc'):
            affichage.affichageNMDS2(scaled_df, nbcandidats, nborders,
                                     avecVotant, nomCandidats, tabOrders)

        elif (path[-4:] == '.csv'):
            # dans tous les cas, on n'affiche pas les votants (le graphe serait illisible)
            affichage.affichageNMDS2(scaled_df, nbcandidats, nborders, 0,
                                     nomCandidats, tabOrders)

        plt.show()

        # evaluation
        eval = affichage.evaluation()

        if eval == 'o':
            time.sleep(0.75)
            candidats, votants = evaluation.NMDStoDict(scaled_df, 2,
                                                       nbcandidats, tabOrders)
            tau = evaluation.evaluer(candidats, votants, nbcandidats, nborders,
                                     tabOrders, 1)
            print('tau = ' + str(tau))
            time.sleep(0.75)

    # Methode : NMDS en dimension 1
    if choix == '4':

        scaled_df = methodeNMDS1.methodeNMDS1(nbcandidats, tabOrders)

        # affichage
        afficheVotant = affichage.affichagAvecVotants()
        avecVotant = 0
        if afficheVotant == 'o':
            avecVotant = 1

        affichage.affichageNMDS1(scaled_df, nbcandidats, nborders, avecVotant,
                                 nomCandidats, tabOrders)

        plt.show()

        # evaluation
        eval = affichage.evaluation()

        if eval == 'o':
            time.sleep(0.75)
            candidats, votants = evaluation.NMDStoDict(scaled_df, 1,
                                                       nbcandidats, tabOrders)
            tau = evaluation.evaluer(candidats, votants, nbcandidats, nborders,
                                     tabOrders, 1)
            print('tau = ' + str(tau))
            time.sleep(0.75)

    # Conclusion sur les temps d'execution des 2 methodes
    if choix == '5':

        graph.courbeTests(temps)

    choix, temps = affichage.menu_methode()

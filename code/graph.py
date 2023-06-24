"""
  Fichier qui realise une analyse sur le temps de calculs des methodes
"""

import lecture
import methodePM2
import methodeNMDS2
import evaluation

import statistics
import time
import matplotlib.pyplot as plt


def courbeTests(temps):
    """Affiche les courbes temps d'exécution/nombre de candidats pour les méthodes 
  PM2 (rouge) et NMDS2 (bleu) avec les fichiers soc 'solved'"""

    # Matrice de fichiers avec premiere case de chaque ligne = nb de candidats

    path = [[
        5, '00049-000001219.soc', '00049-0000012123.soc',
        '00049-0000012130.soc', '00049-0000012125.soc', '00049-0000012111.soc',
        '00049-0000012115.soc'
    ],
            [
                6, '00049-000000259.soc', '00049-0000050513.soc',
                '00049-0000050518.soc', '00049-0000002510.soc',
                '00049-0000002511.soc', '00049-0000002512.soc'
            ],
            [
                7, '00009-0000000211.soc', '00009-000000029.soc',
                '00009-0000000210.soc', '00056-0000007710.soc',
                '00056-0000007711.soc', '00056-0000007713.soc'
            ],
            [
                8, '00049-0000003326.soc', '00049-0000003325.soc',
                '00049-0000003315.soc', '00049-0000024513.soc',
                '00049-000006269.soc', '00049-0000025011.soc'
            ]]

    candidats = [path[i][0] for i in range(len(path))]

    # Tableau des moyennes de temps d'execution
    meanPM2 = []
    meanNMDS2 = []
    meantauPM2 = []
    meantauNMDS2 = []

    # Generation de tests :

    # Parcours pour chaque nombre de candidats
    for k in range(len(path)):

        # Tableau des temps d'exécution pour une liste de fichier (avec un même nombre de candidats donné)
        measuresPM2 = []
        measuresNMDS2 = []
        measurestauPM2 = []
        measurestauNMDS2 = []

        # Parcours pour chaque fichier
        for i in range(1, len(path[k])):
            nbcandidats, _, nborders, tabOrders, _ = lecture.read_file(
                "soc/" + path[k][i])

            # Appel a la methode PM2
            startPM2 = time.time()
            dicC, dicV = methodePM2.methodeSigma(nbcandidats, nborders,
                                                 tabOrders, temps)
            endPM2 = time.time()
            measuresPM2.append(endPM2 - startPM2)
            measurestauPM2.append(
                evaluation.evaluer(dicC, dicV, nbcandidats, nborders,
                                   tabOrders, 2))

            # Appel a la methode NMDS
            startNMDS2 = time.time()
            scaled_df = methodeNMDS2.methodeNMDS2(nbcandidats, tabOrders)
            dicC, dicV = evaluation.NMDStoDict(scaled_df, 2, nbcandidats,
                                               tabOrders)

            endNMDS2 = time.time()
            measuresNMDS2.append(endNMDS2 - startNMDS2)
            measurestauNMDS2.append(
                evaluation.evaluer(dicC, dicV, nbcandidats, nborders,
                                   tabOrders, 2))

        # Calcul de moyennes pour le nombre de candidats donné
        meanPM2.append(statistics.mean(measuresPM2))
        meanNMDS2.append(statistics.mean(measuresNMDS2))

        meantauPM2.append(statistics.mean(measurestauPM2))
        meantauNMDS2.append(statistics.mean(measurestauNMDS2))

    # Courbes moyenne de temps d'execution / nombre de candidats
    plt.plot(candidats,
             meanPM2,
             color='red',
             label='Méthode par programmation mathématique en 2D')
    plt.plot(candidats,
             meanNMDS2,
             color='blue',
             label='Méthode Non Metric Multidimentional Scaling 2D')
    plt.xlabel('Candidats')
    plt.ylabel('Temps d\'exécution')
    plt.legend()

    plt.show()

    # Courbes moyenne tau de kendall / nombre de candidats
    plt.plot(candidats,
             meantauPM2,
             color='red',
             label='Méthode par programmation mathématique en 2D')
    plt.plot(candidats,
             meantauNMDS2,
             color='blue',
             label='Méthode Non Metric Multidimentional Scaling 2D')
    plt.xlabel('Candidats')
    plt.ylabel('Tau de Kendall')
    plt.legend()

    plt.show()

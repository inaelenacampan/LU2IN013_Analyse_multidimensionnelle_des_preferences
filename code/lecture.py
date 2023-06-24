"""
  Fichier dedie a la lecture des donnees des fichiers .soc
"""

import re


def read_file(path):
    """Lit le fichier donné par path"""

    file = open(path, "r")

    # La variable qui va contenir le tableau de preferences
    tabOrders = []
    nomCandidats = []

    for line in file:

        if line.startswith('# ALTERNATIVE NAME '):
            nomC = line.split(': ')[1]
            nomCandidats.append(nomC)

        if line.startswith('# NUMBER ALTERNATIVES:'):

            #le nombre de candidats
            nbcandidats = int(
                re.search(r'\d+',
                          line.rpartition(": ")[2]).group())
            print('Nombre de Candidats = ', nbcandidats)

        if line.startswith('# NUMBER VOTERS:'):

            #le nombre de votants
            nbvoters = int(re.search(r'\d+', line.rpartition(": ")[2]).group())
            print('Nombre total de Votants = ', nbvoters)

        if line.startswith('# NUMBER UNIQUE ORDERS:'):

            #le nombre de preferences uniques
            nborders = int(re.search(r'\d+', line.rpartition(": ")[2]).group())
            print('Nombre de preferences distinctes = ', nborders)

        if not line.startswith('#'):
            tabOrder = [int(s) for s in (re.findall(r'\d+', line))]
            if len(tabOrder) > 0:
                tabOrders.append(tabOrder)
            tabOrder = []

        #cas ou il y a plus de 10 preferences, on s'arrete pour gurobi
        if len(tabOrders) > 10:
            nborders = 10
            break

    return [nbcandidats, nbvoters, nborders, tabOrders, nomCandidats]

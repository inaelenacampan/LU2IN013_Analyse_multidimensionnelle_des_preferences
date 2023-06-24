"""
  Fichier dedie a la methode Non Metric Multidimensional Scaling en deux dimensions
"""

import numpy as np
from sklearn.manifold import MDS


def methodeNMDS2(nbcandidats, tabOrders):
    """Fonction de calcul des coordinées par Non Metric Multidimentional Scaling 2D"""

    nbvoters = sum(tabOrders[i][0] for i in range(len(tabOrders)))

    taille = nbcandidats + nbvoters
    matrice = np.zeros((taille, taille))

    # Matrice de dissimilarité carrée et symétrique

    for i in range(len(tabOrders)):

        for j in range(1, len(tabOrders[i])):

            # S'il n y a pas de preference la valeur reste egale a zero
            if (tabOrders[i][j] != -1):

                # Démultiplication par le nombre de votants

                for k in range(tabOrders[i][0]):
                    matrice[k + i + nbcandidats][tabOrders[i][j] - 1] = j
                    matrice[tabOrders[i][j] - 1][k + i + nbcandidats] = j

    # Calcul des coordonnées
    mds = MDS(n_components=2,
              metric=False,
              dissimilarity='precomputed',
              normalized_stress='auto')

    results = mds.fit(matrice)
    print("Stress : ", results.stress_, "\n")

    scaled_df = mds.fit_transform(matrice)

    return scaled_df

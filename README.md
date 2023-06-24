# Analyse multidimensionnelle des preferences, et applications aux donnees de vote
> Auteurs : Ida Rogie, Ina Campan et Sira Lina Achouri
> 
> Encadrant : Olivier Spanjaard
> 
> Projet realise dans le cadre du module LU2IN013 (Projet de developpement, niveau L2), parcours double licence mathematiques-informatique.


## Version Python requise : python 3.9
## Licence pour le solveur [Gurobi](https://www.gurobi.com/) 10.0.1 : API Python

## I. Bibliotheques utilisees

```python
# pour les 2 methodes utilisees

import gurobipy as gp
from sklearn.manifold import MDS

# pour realiser la lecture des fichiers contenant les donnees

from pathlib import Path
import re

# pour les affichages et manipulations de donnees

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import statistics
import math
from random import *
import time
import scipy.stats as stats
```

## II. Structure du code

### 1. Pour la manipulation des fichiers contenant les donnees :

```python
lecture.py
lectureVote.py
```

### 2. Fichiers *methodes*, groupes selon la dimension souhaitee pour la solution:

```python
methodePM1.py
methodePM2.py
methodeNMDS1.py
methodeNMSD2.py
methodeVote.py
```

### 3. Pour l'affichage du menu et des graphes :

```python
affichage.py
```

### 4. Le main du programme (l'interface):

```python
main.py
```

## III. Compilation

+ Utiliser le fichier main.py et suivre les instructions fournies par le menu
+ Remarque (1) : Le nom du fichier doit etre fourni sans des espaces (avant/apres)!
+ Remarque (2) : Fournir seulement le nom d'un fichier de type *.soc* (profil de preferences completes) ou *.csv* (pour l'application aux donnees de vote)!
+ Remarque (3) : `normalized_stress='auto'` (fichiers `methodeNMDS1.py` et `methodeNMDS2.py`) peut generer une erreur sur certains ordinateurs sous IOS : `TypeError: __init__() got an unexpected keyword argument 'normalized_stress'`. Dans ce cas, il faut supprimer cette partie du code.

## IV. Classification des fichiers utilises pour les tests

### 1. Fichiers **_.soc_**, contenant des profils de preferences completes (librairies de préférences [PrefLib](https://www.preflib.org/datasets))

+ Preferences des etudiants concernant le choix de cours (AGH Course Selection) : `00009-00000001.soc` & `00009-00000002.soc`
+ Classement de boxeurs (Boxing World Rankings) : `00042-xxxxxxxx.soc`
+ Petit-dejeuner (Breakfast Items) : `00035-xxxxxxxx.soc`
+ Recherches sur Internet (Clean Web Search & Web Search) : `00015-xxxxxxxx.soc` & `00011-xxxxxxxx.soc`
+ Enquete en informatique (Education Surveys in Informatics -Cujae) : `00032-xxxxxxxx.soc`
+ Courses de Formule 1 (Formula 1 Races) : `00053-xxxxxxxx.soc`
+ Saisons de Formule 1 (Formula 1 Seasons) : `00052-xxxxxxxx.soc`
+ Classement Global des Universites (Global University Ranking) : `00046-xxxxxxxx.soc`
+ Points turcs mecaniques (Mechanical Turk Dots) : `00024-xxxxxxxx.soc`
+ Puzzle turc mecanique (Mechanical Turk Puzzle) : `00025-xxxxxxxx.soc`
+ Classement des ville Movehub (Movehub City Ranking) : `00050-xxxxxxxx.soc`
+ Competitions multitours (Multilaps Competitions) : `00049-xxxxxxxx.soc`
+ Prix Netflix (Netflix Prize Data) : `00004-xxxxxxxx.soc`
+ Classement equipes de baseball (Seasons/Weeks Power Ranking) : `00056-xxxxxxxx.soc` & `00054-xxxxxxxx.soc`
+ Competitions de patinage (Skate Data) : `00056-xxxxxxxx.soc`
+ Classement Spotify par pays (Spotify Countries Chart) : `00048-xxxxxxxx.soc` & `00047-xxxxxxxx.soc`
+ Preferences Sushi (Sushi Data) : `00014-xxxxxxxx.soc`
+ T-shirt : `00012-xxxxxxxx.soc`
+ Classement tennis de table (Table Tennis Ranking) : `00044-xxxxxxxx.soc`
+ Classement tennis (Tennis Ranking) : `00045-xxxxxxxx.soc`


### 2. Fichiers **_.csv_**, contenant des profils de preferences incompletes (application aux donnees de voter du projet [VoterAutrement](https://vote.imag.fr/results))

```python
# candidats a l'election presidentielle de 2017

stv111.csv
stv411.csv
```

## V. Evaluation
Un **_tau_** 0 indique une representation parfaite et donnees; ainsi un tau egal a 1 indique un dessacord complet entre les preference initiales et celles obtenues a partir de la representation sur le plan.

## VI. Bibliographie
+ [A multidimensional spatial model for preference representation in multi-criteria decision aiding](https://hal.science/hal-03782818/file/A_KHANNOUSSI_et_al_Multidimensional_spatial_model.pdf)
# **Documentation technique d'EduBang**

Ce fichier décrit le mode d'utilisation d'Edubang ainsi que son fonctionnement.

- [Mode d'utilisation](#mode-dutilisation)
- [Code source](#code-source)

# Mode d'utilisation

## Première installation

### Windows 10 et plus

1. Installer Python [3.12.5](https://www.python.org/downloads/release/python-3125/) ou plus.
2. Démarrer EduBang en exécutant le fichier [start.bat](/start.bat), ce fichier installera toutes les dépendances puis exécutera EduBang.

### MacOS

1. Installer Python [3.12.5](https://www.python.org/downloads/release/python-3125/) ou plus.
2. Installer toutes les dépendances qui se trouvent dans le fichier [requirements.txt](/requirements.txt) avec pip.
3. Démarrer EduBang en exécutant le fichier [main.py](/sources/main.py)

---

Utiliser le menu pour naviguer dans le logiciel. Aidez-vous du [plan du logiciel](#plan-du-logiciel)

- [Découvrir](#découvrir)
- [Éditeur de système](#éditeur-de-système)
- [Paramètres](#paramètres)
- [Quitter](#quitter)

## Découvrir

Ce menu vous permet de choisir un système à visualiser. <br/>
Pour choisir un système, **Effectuer un clique gauche sur le système désiré**.

Le logiciel vous redirigera par la suite dans le [Bac à sable](#bac-à-sable).

## Éditeur de système

À RÉDIGER

## Paramètres

Ce menu vous propose de modifier le volume de la musique.

- [Contrôles](#contrôles)

## Quitter

Ce bouton ferme EduBang.

## Bac à sable

Ce menu permet de visualiser le système étudié. <br/>
Il fourni des outils et des données tels que :
- Une échelle de temps en jour par seconde.
- L'affichage des noms des astres.
- L'affichage des trajectoires.
- L'affichage de la norme d'attraction.
- L'affichage d'une prédiction.
- L'affichage du barycentre du système.
- Une règle de mesure
- Le temps écoulé depuis le début de la simulation

Si vous choissisez d'étudier un astre, le bac à sable vous donnera les données relatifs à cet astre tels que :
- La période de révolution autour de l'astre dominant.
- La vitesse orbitale.
- Le rayon.
- La masse.
- La gravité de surface.

## Contrôles

Ce menu vous permet de modifier les associations de touches.

Pour modifier une touche, **Effectuer un clique gauche sur une association de touche** <br/>
puis **Presser la touche désirée**.

À noter que *pour Windows*, les touches **Contrôle** (Ctrl), **Alternative** (Alt), **Delete** (Del), **Tabulation** (Tab), **Espace** sont supportées. <br/>
Vous pouvez faire une association de touche en les combinants.
> Exemple: Ctrl + S, Alt + Del, Ctrl + Alt + Espace, etc.

*Pour MacOS*, les touches **Commande** (Cmd), **Alternative** (Alt), **Tabulation** (Tab), **Espace** sont aussi supportées.

## Plan du logiciel
```
Menu
├── Découvrir
├── Éditeur de système
├── Paramètres
│   └── Contrôles
└── Quitter
```

À noter que le contenu de l'écran _Découvrir_ dépend des systèmes qui ont été créés. <br/>
Par défaut, il existe un système "Solar System", représentant notre système solaire.

# Code source

L'entièreté du code source d'EduBang se trouve dans le répertoire [_sources_](/sources/). <br/>
EduBang nécessite une version de Python supérieur ou égale à [**3.12.5**](https://www.python.org/downloads/release/python-3125/). <br/>
EduBang a besoin des modules suivants pour fonctionner :
- [pygame](https://pypi.org/project/pygame/)
- [pillow](https://pypi.org/project/pillow/)
- [proto-obj](https://pypi.org/project/proto-obj/)
- [nsi25perlin](https://pypi.org/project/nsi25perlin/)
- [eventListen (0.0.5)](https://pypi.org/project/eventListen/0.0.5/)

## Configurations

EduBang est un logiciel de simulation d'astronomie, **elle est sujette à consommer davantage de ressources**, notamment sur le processeur. <br/>
Il est donc important d'avoir une configuration correcte pour pouvoir profiter entrièrement d'Edubang.

|                        | Configuration minimale | Configuration optimale           |
|------------------------|------------------------|----------------------------------|
| Système d'exploitation | Windows 10, macOS      | Windows 10/11, macOS                |
| Processeur             | Dual Core 2.7 GHz      | Intel Core i5 ou Ryzen 5 ou plus |
| Matériel               | Clavier, Souris                | Clavier, Pavé numérique, Souris  |
| Notes supplémentaires  | Aucun                  | Un casque audio ou des enceintes <br/> sont recommandés. |

## Organisation du code

Le fichier [main.py](/sources/main.py) est le fichier principal, c'est lui qui gère PyGame et tous nos composants. <br/>
**Pour démarrer EduBang, exécutez ce fichier.**

---

### Répertoire _window_

Le répertoire _window_ sert à classer les écrans (ou pages) que comporte Edubang.
> Exemple: le menu, les paramètres, le bac à sable, etc.

Les fichiers qu'il contient sont les écrans.
Un écran, pour Edubang, est un fichier Python contenant trois fonctions majeures et obligatoires :
- [load](#load)
- [update](#update)
- [draw](#draw)

Ces fonctions n'ont pas besoin d'arguments ni de retour de valeur, ce sont des routines. <br/>
**Seule la routine draw a un argument (screen, du type pygame.Surface).**

#### **Load**
Le load (ou le loader) est la routine qui sert à charger le contenu d'un écran.
> Exemple: Générer le bruit de perlin, ajouter des boutons sur l'interface, mettre en route certains composants comme la caméra ou la physique.

#### **Update**
L'update est une routine qui est appelée à chaque rafraichissement d'écran pour mettre à jour certains composants nécessitant un rafraaichissement.
> Exemple: La physique.

#### **Draw**
Le draw est la routine qui la dessiner les éléments sur l'écran.
C'est une routine qui dépend de screen, un argument qui a pour valeur l'écran PyGame. (pygame.Surface)

---

### Répertoire _shared_

Le répertoire _shared_ est le répertoire qui contient les composants d'Edubang.

#### Components

C'est le répertoire qui contient les fichiers relatifs à la physique de la simulation.

#### Utils

C'est un répertoire qui contient le fichier utils.py.
Ce fichier est le fichier qui nous sert à créer les éléments d'interface.
> Exemple: Bouton, Input, SlideBar, etc.

Il nous sert aussi à exporter des fonctions physiques, des fonctions relatifs à la génération de l'espace, des constantes, etc.
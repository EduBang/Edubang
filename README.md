![EduBang Logo](https://cdn.faune67.fr/assets/edubang_logo.png)

# EduBang

EduBang est un logiciel développé en Python dans le cadre des [Trophées NSI](https://trophees-nsi.fr/), permettant de **simuler des interactions spatiales** entre astres selon la [loi universelle de la gravitation de Newton](https://fr.wikipedia.org/wiki/Loi_universelle_de_la_gravitation). Ce logiciel offre une représentation réaliste des trajectoires et forces gravitationnelles dans l’espace.

Il permet de **créer des systèmes stellaires** personnalisés en ajoutant des astres tels que des étoiles, des planètes ou des lunes avec des paramètres définis comme la masse, la position ou la vitesse. Cette personnalisation offre une grande liberté créative pour explorer différents scénarios.

EduBang propose aussi **un espace d’expérimentation** où les utilisateurs peuvent modifier les caractéristiques physiques des astres et observer les conséquences sur le système, renforçant ainsi la compréhension des lois de la gravité par la pratique.

Conçu pour être intuitif et captivant, EduBang s’adresse aux élèves, enseignants et passionnés d’astronomie, combinant apprentissage scientifique et plaisir de la découverte.

# **Documentation technique d'EduBang**

Cette partie décrit le mode d'utilisation d'Edubang ainsi que son fonctionnement.

- [Mode d'utilisation](#mode-dutilisation)
- [Code source](#code-source)

# Mode d'utilisation

## Première installation

### Windows 10 et plus

1. Installer Python [3.10.7](https://www.python.org/downloads/release/python-3107/) ou plus.
2. Démarrer EduBang en exécutant le fichier [start.bat](/start.bat), ce fichier installera toutes les dépendances puis exécutera EduBang.

### macOS

1. Installer Python [3.10.7](https://www.python.org/downloads/release/python-3107/) ou plus.
2. Démarrer EduBang en exécutant le fichier [start.command](/start.command), ce fichier installera toutes les dépendances puis exécutera EduBang.

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



L'**éditeur de système** d'EduBang permet de créer et personnaliser des systèmes stellaires en ajoutant des astres (étoiles, planètes, lunes) avec des paramètres définis comme la masse, la position et la vitesse. Il offre une interface interactive pour expérimenter et observer les effets des modifications sur les trajectoires des astres.

Il fournit des outils et des données tels que :
- L'affichage sous forme de grille dynamique
- Deux axes, abscisses et ordonnées gradués permettant de mesurer des distances
- Une bibliothèque de planètes pré-paramétrées
- Une fonction intelligente de sélection des astres
- L'affichage des prédictions dynamique
- Des vecteurs propres à chaque planète pour régler se vitesse
- L'affichage du barycentre du système


Si vous choisssez d'étudier un astre, l' éditeur de système vous donnera les données relatives à cet astre tels que :
- Le rayon.
- La masse.

L'éditeur propose également des fonctionnalités de personnalisation des astres séléctionés:
- Personnalisation de la masse
- Personnalisation du rayon


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

Si vous choisssez d'étudier un astre, le bac à sable vous donnera les données relatifs à cet astre tels que :
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

*Pour macOS*, les touches **Commande** (Cmd), **Alternative** (Alt), **Tabulation** (Tab), **Espace** sont aussi supportées.

## Plan du logiciel
```
Menu
├── Découvrir
│   └── Système stellaire
├── Éditeur de système
├── Paramètres
│   ├── Contrôles
│   └── Langues
└── Quitter
```

À noter que le contenu de l'écran _Découvrir_ dépend des systèmes qui ont été créés. <br/>
Par défaut, il existe un système "Solar System", représentant notre système solaire.

# Code source

L'entièreté du code source d'EduBang se trouve dans le répertoire [_sources_](/sources/). <br/>
EduBang nécessite une version de Python supérieur ou égale à [**3.10.7**](https://www.python.org/downloads/release/python-3107/). <br/>
EduBang a besoin des modules suivants pour fonctionner :
- [pygame (2.6.1)](https://pypi.org/project/pygame/2.6.1)
- [pillow (11.1.0)](https://pypi.org/project/pillow/11.1.0)
- [proto-obj (0.0.4)](https://pypi.org/project/proto-obj/0.0.4)
- [nsi25perlin (0.0.2)](https://pypi.org/project/nsi25perlin/0.0.2)
- [eventListen (0.1.2)](https://pypi.org/project/eventListen/0.1.2/)

## Configurations

EduBang est un logiciel de simulation d'astronomie, **elle est sujette à consommer davantage de ressources**, notamment sur le processeur. <br/>
Il est donc important d'avoir une configuration correcte pour pouvoir profiter entrièrement d'Edubang.

|                        | Configuration minimale | Configuration optimale           |
|------------------------|------------------------|----------------------------------|
| Système d'exploitation | Windows 10, macOS      | Windows 10/11, macOS             |
| Processeur             | Dual Core 2.7 GHz      | Intel Core i5 ou Ryzen 5 ou plus |
| Matériel               | Clavier, Souris        | Clavier, Pavé numérique, Souris  |
| Notes supplémentaires  | Aucun                  | Un casque audio ou des enceintes <br/> sont recommandés. |

## Organisation du code

Le fichier [main.py](/sources/main.py) est le fichier principal, c'est lui qui gère PyGame et tous nos composants. <br/>
**Pour démarrer EduBang, exécutez ce fichier.**

---

### Répertoire _/window_

Le répertoire _/window_ sert à classer les écrans (ou pages) que comporte Edubang.
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

### Répertoire _/shared_

Le répertoire _/shared_ est le répertoire qui contient les composants d'Edubang.

#### Répertoire _/components_

C'est le répertoire qui contient les fichiers relatifs à la physique de la simulation.

#### Répertoire _/utils_

C'est un répertoire qui contient le fichier utils.py.
Ce fichier est le fichier qui nous sert à créer les éléments d'interface.
> Exemple: Bouton, Input, SlideBar, etc.

Il nous sert aussi à exporter des fonctions physiques, des fonctions relatifs à la génération de l'espace, des constantes, etc.

# **Auteurs**

- [Anaël Chevillard](https://github.com/anaelchevillard)
- [Sacha Freguin](https://github.com/AS-Pic)
- [Néji Lim](https://github.com/ArticOff)

# **License**

[GPLv3](https://opensource.org/licenses/)

# Documentation technique d'Edubang

Le code source se trouves dans le répertoire sources. <br/>
Edubang nécessite une version de Python supérieur ou égale à **3.12.5**.

## Organisation du code

Le fichier main.py est le fichier principal, c'est lui qui gère PyGame et tous nos composants. <br/>
Pour lancer Edubang, exécuter ce fichier.

---

### Répertoire _window_

Le répertoire "window" sert à classer les écrans que comporte Edubang.
Exemple: le menu.

Les fichiers qu'il contient sont les écrans.
Un écran, pour Edubang, est un fichier Python contenant trois fonctions majeures:
- load
- update
- draw

Ces fonctions n'ont pas besoin d'arguments ni de retour de valeur, ce sont des routines. <br/>
**Seule la routine draw a un argument (screen, du type pygame.Surface).**

#### **Load**
Le load (ou le loader) est la fonction qui sert à charger le contenu d'un écran.
Exemple: Générer le bruit de perlin, ajouter des boutons sur l'interface, mettre en route certains composants comme la caméra ou du la physique jeu.

#### **Update**
L'update est une fonction qui est appelée chaque rafraichissement d'écran pour mettre à jour la physique de la simulation.

#### **Draw**
Le draw est la fonction qui la dessiner les éléments sur l'écran.
Elle a un argument screen qui a pour valeur l'écran pygame. (pygame.Surface)

---

### Répertoire _shared_

Le répertoire "shared" est le répertoire qui contient les composants d'Edubang.

#### Components

C'est le répertoire qui contient les fichiers relatifs à la physique de la simulation.

#### Utils

C'est un répertoire qui contient le fichier utils.py.
Ce fichier est le fichier qui nous sert à créer les éléments d'interface
Exemple: Bouton, Input, SlideBar, etc.

Il nous sert aussi à exporter des fonctions physiques, le bruit de Perlin, les vecteurs, etc.

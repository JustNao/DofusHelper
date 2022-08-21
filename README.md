# Avertissement

Tous les scripts utilisent des IDs de packet qui sont très souvent changés par Ankama. Ils nécessitent donc une mise à jour manuelle pour fonctionner.
Je ne joue pas régulièrement donc les IDs sont rarement exactes; je laisse quand même les scripts pour ceux que ça intéresse, si vous tombez sur un bon moment et j'ai mis à jour récemment, ou si vous voulez vous-même mettre à jour les IDs (les scripts que j'utilise pour le faire sont ceux de LaBot, lien tout en bas).

My process for extracting packet IDs (every script used is from [Labot](https://github.com/louisabraham/LaBot)) :

1. Decompile the DofusInvoker.swf using scripts/decompile.sh. You may need to modify the Dofus folder and/or the location of the ffdec depending on the OS. On Windows, don't forget to put the path to ffdec.exe in double quotes.
   This will decompile every packet file into the protocol folder
2. Build the protocol.pk using scripts/built_protocol.py

# Dofus Help Manager

Repo pour diffuser le bot (projet perso).

## Installation

1. Installer [Python 3](https://www.python.org/downloads/)
2. Ajouter PIP (installé avec les dernières versions de Python) [à votre Path](https://www.architectryan.com/2018/03/17/add-to-the-path-on-windows-10/). Si vous n'avez rien touché à l'installation de python, le dossier à ajouter devrait être
   'C:\Program Files\Python39\Scripts'.
3. Installer [Npcap](https://nmap.org/dist) <= 1.60
4. Télécharger le [Chromedriver](https://chromedriver.chromium.org/downloads) qui correspond à votre version de Chrome
5. Ajouter ce Chromedriver à votre PATH
6. Exporter le git (bash, zip, ...)
7. Lancer setup.bat

## Utilisation

Le programme s'éxécute par le fichier main.py.

Soit ouvrir le fichier launch.bat (sous Windows), soit l'ouvrir dans une invite de commande à l'aide de

```bash
py main.py
```

Une fois lancé, vous aurez accès une liste d'outils.

### Treasure Hunt Helper

Localise les indices de chasse au trésor. Une mini fenêtre s'ouvre pour afficher la position, la distance avec la joueur et la direction (style GPS). Détection de phorreur et d'archimonstre intégrée. Cliquer sur l'icône de drapeau, loupe ou combat clique directement sur le bouton respectif dans la fenêtre de chasse au trésor (si celle ci est ouverte). 

### Treasure Hunt Bot

Mêmes fonctionnalités et fenêtre que le helper, mais tout est automatisé (sauf le combat). Les déplacements s'effectuent pas un clic. Pour le bas le bot recherche l'icône de changement de barre de sort, il faut donc que vous soyez à la première page pour le calibrage au lancement de l'application. Pour le reste des déplacements, le milieu de l'écran est pris.

### HDV List

Une fois le sniffer activé, aller dans l'onglet vente d'un hdv va lister tous les items en vente, et les parcourir un par un. Les items qui ne sont pas les moins chers en hdv seront repostés au prix maximal - 1 kamas.

### HDV Missing Items

Lancer le module, aller à l'HDV équipements, et sélectionner toutes les catégories craftables (coiffe, cape, arme, bouclier, etc). Une fois chacune chargée (un message dans la console s'affiche pour chaque sous catégorie), vous pouvez sauvegarder les données, qui seront stockées dans output/missingItems.xlsx.
L'outil écrase les valeurs précédentes à chaque fois, les catégories manquantes dans le chargement seront donc vides.

La version actuelle utilise un GoogleSheets personnel, elle ne marchera donc pas pour vous.
J'ai laissé hdvMissingItems.local.py pour accéder à la version locale (supprimez la nouvelle version et enlevez le .local du fichier).

### Chat Searcher

Scan tous les messages du chat à la recherche de la chaîne de caractère donnée en input. Renvoie le message avec le nom du personnage dans la console. Plusieurs éléments de recherche sont possibles, en les séparant avec un ';'.

### Multicompte Tool

A chaque début de tour dans un combat, ouvre la fenêtre du joueur correspondant. Rentrer dans DHM la liste de tous les personnages jouables. Si la case 'Mule' est cochée, la touche 'V' sera appuyée au changement de fenêtre (raccourci pour passer le tour dans mon cas). Le bouton 'Save' sauvegarde la liste des personnages actuels dans config/multicompte.json.
Pour lancer le module avec les personnages sauvegardés, n'en ajoutez aucun manuellement et lancez le directement.

Le module recupère l'ID de chaque personnage en entrant en combat, et l'associe à un nom de personnage grâce à la fenêtre active. Si vous voulez que le module marche bien, il faut donc que le client du personnage qui entre en combat soit ouvert au moment où celui-ci entre en combat (pas de alt-tab dès que vous cliquez sur un groupe par exemple).

### AvA Counter

Une fois lancé, à chaque changement de map un comptage des joueurs présents par alliance sera fait (utile en cas de AvA où des piles sont faites pour compter le nomber de joueurs).

### Price Computer

Ouvre une mini fenêtre en premier plan. En jeu, envoyez un message de groupe (obligatoirement) avec **$price** suivi d'un link d'item (shift + clic ou clic droit et insérer un item dans le chat). Le prix de craft sera affiché dans la mini fenêtre.

### Price Listing

Liste le prix de tous les items en hdv ressource. Extrêmement lent (+ de 3 heures de scan), et utile pour vous uniquement si vous voulez absolument changer le prix des items en interne. Le prix de chaque item peut se retrouver dans sources/gameRessources/prices.json, trié par l'ID de l'item (que vous pouvez soit retrouver dans les fichiers du jeu, soit sur l'encyclopédie du site dans l'URL de l'item).

### Fail Safe

Dans n'importe quel module, quand le bot pixel est utilisé, placer la souris dans le coin supérieur gauche de l'écran stoppera le bot (il faudra relancer l'application pour relancer le bot).

## Copyright

Merci à [LaBot](https://github.com/louisabraham/LaBot) pour son reader/writer de packet.

## License

[MIT](https://choosealicense.com/licenses/mit/)

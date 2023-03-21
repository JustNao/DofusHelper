

# Avertissement

## Vous pouvez trouver le nouveau projet basé sur Dofus Help Manager sur : [Karrelage](github.com/JustNao/Karrelage)

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
3. Installer [Npcap](https://nmap.org/dist) <= [1.60](https://npcap.com/dist/npcap-1.60.exe)
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

Mêmes fonctionnalités et fenêtre que le helper, mais tout est automatisé (sauf le combat). Par défaut, les déplacements s'effectuent pas un clic. Pour le bas le bot recherche l'icône de changement de barre de sort, il faut donc que vous soyez à la première page pour le calibrage au lancement de l'application. Pour le reste des déplacements, le milieu de l'écran est pris. Un fichier `config.json` est créé à la racine au premier lancement du bot où vous pouvez passer `autopilot` à `true` pour activer le mode monture autopilotée.

### HDV Filter

Charger les ventes d'un équipement en HDV, puis choisir des stats minimums. Les ventes présentes en HDV qui satisfont les conditions sont affichées (flèches gauche et droite pour naviguer).

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

A chaque début de tour dans un combat, ouvre la fenêtre du joueur correspondant.
Le module utilise le fichier `config/multicompte.json` pour récupérer les noms des personnages. Ajoutez vos personnages et enlevez le `_example` pour que le module fonctionne.

Par défaut le module va juste ouvrir la fenêtre du joueur, mais si la valeur `mule` est à `true`, le module va juste envoyer la touche `v` au client (touche pour passer le tour dans mon cas), même si le client est en background. Donc si vous êtes une mule sasa, le module passe le tour tout seul sans que vous ayez à avoir le jeu ouvert. L'interface graphique a un mode on/off qui permet de toggle rapidement le mode "passe-tour", par exemple s'il y a un challenge qui nécessite d'effectuer une action avant de passer.

Cliquer avec le bouton milieu de la souris va envoyer le click sur tous personnages chargés dans le module.

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

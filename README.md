# NAO-Foot-UV27-2018
NAO Soccer Challenge 2018 (UV 2.7)

Base de départ pour la compétition NAO Foot UV 2.7 2017

Pour la mise au point avec le simulateur V-REP, deux scénarios (dans le dossier scenes du répertoire) sont disponibles :  
nao-UV27-2018-one-robot-yellow-ball-save-image.ttt (port 11212)
nao-UV27-2018-two-robots-yellow-ball-save-image.ttt ports 11212 et 11216)

Les fichiers (archives binaires) utiles au projet mais non gérés par git sont :
- pynaoqi-20180402.tgz pour la commande du robot NAO en python 2.7
- naoqi-20180402.tgz      "intelligence" du robot NAO
- v-rep-20180402.tgz      simulateur dynamique V-REP

Ces archives sont à récupérer sur /public/share/uv27spid et à decompresser dans votre projet.
Lorsque vous êtes dans le répertoire principal du projet (en principe NAO-Foot-UV27-2018), vous pouvez ajouter ces fichiers 
avec la commande : 
- . ./copy_usefull_files.bash

Vous pouvez aussi le faire avec les commandes suivantes :
- tar xfz /public/share/uv27spid/pynaoqi-20180402.tgz
- tar xfz /public/share/uv27spid/naoqi-20180402.tgz 
- tar xfz /public/share/uv27spid/v-rep-20180402.tgz

Les équipes sont à définir dans le fichier "teams_n_games.txt"

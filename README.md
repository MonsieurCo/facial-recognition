

# Facial recognition: the mask / no mask case

![](ressources/readmeImages/imageAnnotator.gif)
## Introduction
Le but de ce projet est de réaliser un logiciel d’annotations d’images en
python pour fournir un jeu de données à l’IA de la seconde partie du projet.
Nous avons donné la possibilité à l’utilisateur d’encadrer une
ou plusieurs régions de l’image puis de lui assigner une catégorie. Chaque cadre est éditable, 
on peut changer la catégorie ou supprimer ce dernier au besoin. L’utilisateur
peut sauvegarder toutes ses annotations dans un fichier JSON. 
Il peut également importée d'autres catégories, en ajoutée ou en supprimée.


### Utilisation
NOTE: Pensez à mettre les droits d'éxecution sur le fichier `build.sh` pour installer les dépendances et lancer l'application.

Pour lancer : 
```bash
chmod u+x build.sh
./build.sh
``` 
En étant à la racine du projet.

vérifiez les [requirements](requirements.txt)
  - Python 3.9+
  - Dépendances requises:
    - PySide6==6.2.1
    - Pillow==8.4.0 
    - Shapely==1.8.0
  
 
  - Pour commencer, **ouvrir un fichier ou un dossier** via la menu-bar ou en effectuant un drag and drop sur la zone prévue à cet effet.
![](ressources/readmeImages/dragndropAPP.png)
  - Une fois le dossier ouvert, **ouvrez une image** en double-cliquant dessus et commencez à annoter. 
![](ressources/readmeImages/open.png)
  - Pour **sélectionner une zone** vous pouvez appuyer sur clique-gauche et étirer jusqu'à la taille souhaitée. 
![](ressources/readmeImages/annotation.png)
  - Vous pouvez **sélectionner plusieurs zones** sur une même image, ainsi qu'**ajouter des catégories** via le champ éditable sur le dessus de la liste.
![](ressources/readmeImages/multi.png)
  - Exemple de **json** fourni par le logiciel
 ![](ressources/readmeImages/json-output.png)
  - Pour **supprimer une annotation** faite clique droit sur la zone annotée de l'image.
  - Pour **éditer une annotation** double-cliquez dessus, la fenêtre des choix de catégorie va apparaitre et vous pourrez éditer votre annotation.
  - Pour **éditer une catégorie** double-cliquez dessus pour qu'elle devienne éditable, une fois la modification faite, appuyez sur "Change Category" pour valider le changement, qui se reportera dans le fichier JSON d'annotations.
  - Vous pouvez utiliser les raccourcis usuels : 
      - CTRL + S : pour sauvegarder.
      - CTRL + O : pour ouvrir un fichier.
      - CTRL + SHIFT + O : ouvrir un dossier.
      - CTRL + W : pour quitter une image.
      - CTRL + H : pour ouvrir ce README.


#### contributeurs :
- [Dylann B](https://github.com/takitsu21)
- [Margaux Schmied](https://github.com/margauxschmied)
- [Antoine C](https://github.com/MonsieurCo)



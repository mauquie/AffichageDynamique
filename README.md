# AffichageDynamique
Affichage dynamique du Lycée Bourdelle

## Informations concernant la base de données
Le paramétrage de la base de données a été fait comme cela :
```
Moteur : PostgreSQL
Nom : AffichageDynamiqueDB
Utilisateur : djangoServer
Mot de passe : B0urdelle
Hôte : localhost
Port : 5432
```
Ce sont les informations à utiliser pour créer la base de données chez soi. Si vous êtes ammené à modifier ses informations, dites le et modifiez le README ! (On garde ces valeurs tant qu'il n'y a pas de problème pour le futur serveur, donc chez vous, vous allez créer une DB avec ces informations et non les modifier pour correspondre à votre DB déjà existante, compris ?)

## Informations sur le système d'application de Django
Il y a 3 applications différentes pour le serveur :
1) Une application gérant l'API (nommée ApiServer)
2) Une application gérant l'affichage sur les écrans (nommée Affichage)
3) Une application gérant le côté gestion (nommée WebServer)

Chacune des applications ont une fonction donnée, donc si vous faites l'affichage du self ou celui de la vie scolaire, vous modifirez seulement (sauf grosse exception où il faudra voir avec le groupe) les fichiers dans le dossier "Affichage". Si vous avez besoin d'ajouter des urls (imaginons pour l'API), vous modifirez le fichier nommé urlsApiServer.py (= urlsNOMAPPLICATION.py). Pas de besoin de modifier le fichier urls.py dans AffichageDynamique.

Pour acceder aux différentes applications (via un navigateur), les urls sont formées comme ceci :
1) API : localhost:8000/api/
2) Affichage : localhost:8000/ecran/
3) Web : localhost:8000/

## Utiliser le découpeur d'image
Pour utiliser des images dans les articles, on a du créer un système pour les rogner, les tourner, les bouger etc, en bref les modifier. Pour l'utiliser, il faut quelques prérequis :
1) Un input qui ne peut prendre qu'une image
2) Un DIV sur lequel on cliquera pour obtenir la fenêtre de modification
3) (Optiennel) Un IMG pour afficher une prévisualisation de l'image hors de la fenêtre de modification
4) (Optionnel) Un SVG que l'on veut cacher/afficher en fonction de si l'utilisateur à selectionné une nouvelle image (comme une image par défaut)

Ensuite, du coté HTML, on devra avoir le code formé comme ceci :
```html
<div id="imageUploadBox" data-bs-toggle="" data-bs-target="#staticBackdrop">
    <svg id="svgImage"></svg>
    <div id="imagePreview" hidden></div>
    <input name="image" id="imageInput" type="file" accept="image/*" hidden>
</div>
```
Les données `data-bs-toggle` et `data-bs-target` sont utilisées pour afficher la fenêtre Modal de bootstrap(celle de modification). Il y a deux champs `hidden`, le premier est car on ne veut pas afficher de prévisualisation avant d'avoir une image à afficher, et le second est car on ne veut pas avoir de champ visible pour la sélection de l'image. C'est grâce à notre code qu'on l'affiche la fenêtre de sélection.

Pour que le code fonctionne, il faudra cependant importer d'autres choses. Nous devons d'abord faire un 
```django
{% decoupeur.html %}
``` 
(le lien symbolique peut changer, il se trouve dans Templates/WebServer/), ensuite, nous devrons importer les fichiers javascript :
```html
<script src="{% static 'JS/cropper.js' %}"></script>
<script src="{% static 'JS/imageDecoupeur.js' %}"></script>
```
Et enfin écrire le code suivant :
```javascript
let decoupeur = new imageDecoupeur(document.getElementById("imageInput"), 
    document.getElementById("imageUploadBox"),
    document.getElementById("imagePreview"),
    document.getElementById("svgImage"),
)
```

Maintenant, grâce à cela, nous pouvons utiliser le decoupeur partout dans l'application.
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
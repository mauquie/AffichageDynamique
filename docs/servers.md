# Les différents serveurs 
Pour bien fonctionner, on a crée 3 serveurs qui communique ensemble, [le serveur gérant l'affichage et sa gestion](#gestion-de-laffichage-dynamique), [un serveur qui s'occupe de faire le lien entre Pronote et le premier serveur](#pronoteserver) et le dernier [serveur qui s'occupe de faire le lien entre les élèves et le serveur principal pour les sondages](#serveur-sondage).

![Schema Serveurs](./images/schemaServers.png)

## Gestion de l'affichage dynamique
![Affichage Dynamique](./images/AffichageDynamique.png)

Le serveur est entièrement fait en python grâce au framework Django. Il se lance sur le port 8080 de la machine. Il est découpé en 3 applications : 
- [Affichage](#affichage) 
- [WebServer](#webserver)
- [ApiServer](#apiserver)

### Affichage 
L'application ``Affichage`` est assez simple, elle s'occupe de renvoyer les pages HTML correspondante à l'identifiant d'un l'écran fourni. 

Par exemple, lorsque l'on fait une requête GET vers :
```
localhost/ecran?name=self
```
Elle nous renverra le fichier HTML correspondant à ``self`` à afficher.

Si l'application ne trouve pas de page correspondante, elle renverra un fichier html ``base`` qui nous sert à ne pas laisser un écran noir en plein milieu du lycée s'il y a une maintenance.

### WebServer
L'application ``WebServer`` gére toutes les pages de gestion des écrans. Par exemple, celle pour ajouter un [article](user.md#les-articles) ou celle pour ajouter des [informations](user.md#les-informations).

Arboréscence des urls et leur définition: [ici](api/webServer.md)
### ApiServer
L'application ``ApiServer`` quant à elle s'occuper de gérer et de retourner les données demandées sous format JSON. Les données concernent uniquement les écrans, c'est à dire que les requêtes atteignant cette application proviennent uniquement des écrans.

Documentation de l'api : [ici](./api/apiServer.md)

## PronoteServer
![Pronote Server](./images/pronoteServer.png)

Le serveur est entièrement fait en nodeJS avec le module [pronote-api](https://github.com/dorian-eydoux/pronote-api). Le module étant seulement en nodeJS nous avons préféré faire un serveur secondaire qui fera le lien entre pronote et le serveur `Affichage dynamique`. Ce serveur n'est disponible seulement en local pour des raisons de sécurités.

Le serveur se connecte à pronote avec des identifiants donnés, garde une session n'ayant pas de limite dans le temps et fait des requêtes vers Pronote quand on demande une ressource provenant de Pronote, pour être sûr d'être à jour. Si jamais il y a un problème avec le serveur Node, chaque resultat de requête est sauvegardé dans la base de données pour permettre de quand même retourner une valeur.

Pour le moment le serveur récupère seulement les profs absents et les menus de la date demandée (si la date n'est pas précisée, par defaut ça sera la date d'aujourd'hui qui sera utilisée)

Le serveur tourne sur le port 5000 en http.

Documentation de l'api disponible [ici](./api/pronoteServer.md)

## Serveur sondage

Le serveur sondage est entièrement consacré à faire le lien entre les élèves et le [serveur AffichageDynamique](#gestion-de-laffichage-dynamique). Il sert d'intermédiaire.

Il est programmé en Python (Django) et il se lance sur le port 8080 de la machine.

Il a 2 vues (views), une qui donne la page de vote, et l'autre qui post les données sur le serveur AffichageDynamique à l'adresse /api/postVote.

Documentation des views [ici](./api/sondageServer.md)
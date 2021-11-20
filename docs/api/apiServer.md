# Documentation de ApiServer
Ceci est la documentation de l'application [ApiServer](../servers.md#apiserver)
 
## Terminaisons 
>___
>#### `api/menus` -> JSON
>##### GET
>Récupère les menus depuis le serveur pronote ou s'il est indisponible depuis la base de données et les renvoie en JSON
>___
>#### `api/articles` -> JSON
>##### GET
>Récupère les articles pas encore [périmer](../user.md#une-date-de-péremption) et les renvoie en JSON
>___
>#### `api/infos` -> JSON
>##### GET
>Récupère les informations / annonces pas encore [périmer](../user.md#une-date-de-péremption) et les renvoie en JSON
>___
>#### `api/displays` -> JSON
>##### GET
>Récupère les écrans et leur page et les renvoie en JSON
>___
>#### `api/profsAbs` -> JSON
>##### GET
>Récupère les profs absents de la journée et les renvoie en JSON
>___

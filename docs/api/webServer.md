# WebServer Terminaisons
Ici se trouve toutes les terminaisons de l'application [WebServer](../servers.md#webserver)

## Arboréscence
```text
WebServer
    ├──articles
    │   ├──ajouter
    │   ├──modifier
    │   ├──toggleVisibilite
    │   └──supprimer
    ├──parametres
    │   ├──informations
    │   │   ├──ajouter
    │   │   ├──modifier
    │   │   ├──supprimer
    │   │   └──toggleVisibilite
    │   ├──ecrans
    │   │   ├──ajouter
    │   │   ├──modifier
    │   │   └──supprimer
    │   ├──pages
    │   │   ├──ajouter
    │   │   ├──modifier
    │   │   └──supprimer
    │   ├──sondages
    │   │   ├──ajouter
    │   │   ├──modifier
    │   │   ├──voirResultats
    │   │   ├──toggleVisibilite
    │   │   └──supprimer
    │   └──modifierPageEcran
    ├──comptes
    │   ├──ajouter
    │   ├──modifier
    │   ├──toggleActive
    │   └──voir
    ├──login
    ├──firstLogin
    ├──logout
    └──resetPassword
```

## Définitions
- [Articles](#articles)
- [Paramètres](#paramètres)
- [Comptes](#comptes)
- [Autres](#autres)
### Articles
>___
>#### `articles` -> HTML
>##### GET
>Liste de tous les articles postés avec les actions possibles à faire
>___
>
>#### `articles/ajouter` -> HTML
>##### GET
>Recupère la page pour poster un article
>##### POST
>Poste l'article sur le site
>___
>#### `articles/modifier?id=` -> HTML
>##### GET
>Recupère la page pour modifier l'article correspondant à `id`
>##### POST
>Poste l'article sur le site
>___
>#### `articles/supprimer?id=` -> Redirect
>##### GET
>Supprime l'article correspondant à `id`
>___
>#### `articles/toggleVisibilite?id=` -> Redirect
>##### GET
>Change la visibilité de l'article correspondant à `id`
>___

### Paramètres
#### Informations
>___
>#### `parametres/informations` -> HTML
>##### GET
>Liste toutes les informations / annonces mise en ligne sur le site
>___
>#### `parametres/informations/ajouter` -> HTML
>##### GET
>Récupère la page pour ajouter une information
>##### POST
>Poste l'information / annonce sur le site
>___
>#### `parametres/informations/modifier?id=` -> HTML
>##### GET
>Récupère la page pour modifier une information correspondant à `id`
>##### POST
>Poste l'information / annonce sur le site
>___
>#### `parametres/informations/supprimer?id=` -> Redirect
>##### GET
>Supprime l'information correspondante à `id`
>___
>#### `parametres/informations/toggleVisibilite?id=` -> Redirect
>##### GET
>Change la visibilite de l'information correspondante à `id`
>___

#### Ecrans
>___
>#### `parametres/ecrans/ajouter` -> HTML
>##### GET
>Récupère la page pour ajouter un ecran
>##### POST
>Ajoute l'ecran sur le site
>___
>#### `parametres/ecrans/modifier?id=` -> HTML
>##### GET
>Récupère la page pour modifier un ecran correspondant à `id`
>##### POST
>Met à jour l'ecran sur le site
>___
>#### `parametres/ecrans/supprimer?id=` -> Redirect
>##### GET
>Supprime l'ecran correspondant à `id`
>___
#### Pages
>___
>#### `parametres/pages/ajouter` -> HTML
>##### GET
>Récupère la page pour ajouter une page
>##### POST
>Ajoute la page sur le site
>___
>#### `parametres/pages/modifier?id=` -> HTML
>##### GET
>Récupère la page pour modifier une page correspondant à `id`
>##### POST
>Met à jour la page sur le site
>___
>#### `parametres/pages/supprimer?id=` -> Redirect
>##### GET
>Supprime la page correspondant à `id`
>___
#### Autre
>___
>#### `parametres/modifierPageEcran` -> HTML
>##### GET
>Récupère la page pour modifier l'affectation entre un ecran et de la page qu'il affiche
>##### POST
>Met à jour l'affectation de la page à (aux) l'écran choisi
>___
#### Sondages
>___
>#### `parametres/sondages` -> HTML
>##### GET
>Liste toutes les sondages mit en ligne sur le site
>___
>#### `parametres/sondages/ajouter` -> HTML
>##### GET
>Récupère la page pour ajouter un sondage
>##### POST
>Poste le sondage sur le site
>___
>#### `parametres/sondages/modifier?id=` -> HTML
>##### GET
>Récupère la page pour modifier un sondage correspondant à `id`
>##### POST
>Poste le sondage sur le site
>___
>#### `parametres/sondages/supprimer?id=` -> Redirect
>##### GET
>Supprime le sondage correspondant à `id`
>___
>#### `parametres/sondages/toggleVisibilite?id=` -> Redirect
>##### GET
>Change la visibilite du sondage correspondante à `id`
>___
>#### `parametres/sondages/voirResultats?id=` -> HTML
>##### GET
>Donne la page affichant les resultats d'un sondage
>___
### Comptes
>___
>#### `comptes` -> HTML
>##### GET
>Liste de tous les articles postés avec les actions possibles à faire
>___
>
>#### `comptes/ajouter` -> HTML
>##### GET
>Recupère la page pour ajouter un compte
>##### POST
>Ajoute le compte sur le site
>___
>#### `comptes/modifier?id=` -> HTML
>##### GET
>Recupère la page pour modifier le compte correspondant à `id`
>##### POST
>Met à jour le compte sur le site
>___
>#### `comptes/toggleActive?id=` -> Redirect
>##### GET
>Change la visibilité du compte correspondant à `id`
>___
>#### `comptes/voir?id=` -> HTML
>##### GET
>Recupère la page affichant les données d'un compte
>___
### Autres
>___
>#### `login` -> HTML
>##### GET
>Recupère la page pour se connecter
>##### POST
>Tente de connecter le compte donné
>___
>#### `firstLogin` -> HTML
>##### GET
>Recupère la page pour modifier le mot de passe correspondant`
>##### POST
>Met à jour le mot de passe et redirige vers le site
>___
>#### `logout` -> Redirect
>##### GET
>Deconnecte l'utilisateur
>___
>#### `resetPassword?id=` -> Redirect
>##### GET
>Réinitialise le mot de passe du compte correspondant à `id`
>___
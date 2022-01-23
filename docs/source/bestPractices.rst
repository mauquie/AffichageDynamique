Autres
================

.. toctree::
    :maxdepth: 2
    :hidden: 

    environ

Bonnes pratiques
----------------

Les bonnes pratiques à suivre pour faire perdurer au mieux ce projet:

(elles ne sont pas là pour vous faire chier mais pour que tout fonctionne
encore longtemps comme la documentation sphinx qui se génère quasi 
automatiquement depuis les commentaires des fonctions ou autre)

* Tout le code est en anglais 
* Tous les commentaires sont en français
* Tous les commentaires suivent la règle d'écriture Google Style
* Chaque modification de la BDD doit être aussi faite sur ce `schema <https://docs.google.com/drawings/d/1yCdKcljLSONPLhfrOhq5kneu9itC2eBE0EqdtVylxFo/edit?usp=drive_web&ouid=111429135849823238093>`_
* Chaque tâche peut être répertoriée dans le Botion prévu à cet effet

Différentes commandes
---------------------

Créer les documentations
________________________

Pour créer les documentations rien de plus simple, on exécute les commandes :

.. code-block:: console

    $ cd docs/
    $ make clean
    $ rm -r source/generated/*
    $ python makeDocs.py

Ici on supprime les anciennes versions de la documentation et on reconstruit 
tout depuis le debut

.. _populatedb:

python manage.py populate_db
____________________________

Cette commande a pour but d'ajouter toutes les valeurs par défaut au serveur.
Pour l'instant seules celles necéssaires sont ajoutées mais bientot même les 
valeurs de DEBUG le seront.

Elle prend le fichier ``data.json`` qui se trouve à la racine du projet 
(il n'est pas partagé pour des raisons de sécurité) et ajoute les valeurs
qui se trouvent à l'intérieur.

Environnement variables
_______________________

Fichier s'occupant de récupérer les valeurs du .env pour les settings du projet 

:doc:`environ`
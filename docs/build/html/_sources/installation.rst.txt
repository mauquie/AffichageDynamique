Installation
============

.. _installation:

Dépendances pour lancer le projet
---------------------------------

Pour utiliser le projet, il faut d'abord installer ces dépendances :

.. code-block:: console

   $ sudo apt install python3.8-venv libpq-dev python3-dev

Créer un environnement et l'activer :

.. code-block:: console

   $ python -m venv .venv
   $ source .venv/bin/activate

Installer les dépendances python:

.. code-block:: console

   $ pip install -r requirements.txt

Et installer les dépendances nodeJS:

.. code-block:: console

   $ cd PronoteServer/
   $ npm install -y
   $ cd ..

Configuration
-------------

Ce n'est pas tout, pour lancer le projet il faut donner les valeurs par 
défauts du fichier ``.env``

.. warning::
   Ces informations sont confidentielles et ne doivent pas être divulgées !


.. literalinclude:: ../../.env.example
  :language: text

.. rubric:: Explication :

* Pronote
   Identifiants pronote utilisé par pronoteServer pour s'y connecter et 
   récupérer les informations

* Auth Ldap
   Informations LDAP pour utiliser les utilisateurs déjà enregistrés dans la 
   base de données, utilisé par djangoServer

* DB
   Identifiants de la base de données utilisée par le projet. 
   Doit nécessairement être une base de données `PostgreSQL`

* Twitter token
   Token twitter que djangoServer utilise pour récupérer les derniers tweets 
   du compte du lycée

* Meteo token 
   Token OpenWeatherMap que djangoServer utilise pour récupérer les infos sur 
   la météo


Une fois le tout configuré, vous pouvez exécuter la commande :

.. code-block:: console

   $ cd AffichageDynamiqueServer/
   $ python manage.py populate_db

Référence : :ref:`populatedb`

Qui aura pour effet d'ajouter toutes les valeurs initiales pour que le serveur
fonctionne comme prévu (par exemple il ajoute seul les permissions 
supplémentaires et les différents types d'informations) 
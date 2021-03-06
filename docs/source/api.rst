API End Points
================

Tous les points de sortie
-------------------------

.. list-table:: Tableau des urls de l'api
   :widths: 20 20 20 20 20
   :header-rows: 1

   * - Objet
     - Methode
     - Url
     - Explication
     - Fonction appelée

   * - Articles
     - GET
     - /api/articles
     - :ref:`Get Articles <getArticles>`
     - :py:func:`ApiServer.views.getArticles`

   * - Informations
     - GET
     - /api/informations
     - :ref:`Get Informations <getInfos>`
     - :py:func:`ApiServer.views.getInfos`

   * - Surveys
     - GET
     - /api/sondages
     - :ref:`Get Surveys <getSurveys>`
     - :py:func:`ApiServer.views.getSurveys`

   * - Displays
     - GET
     - /api/displays
     - :ref:`Get Displays <getDisplays>`
     - :py:func:`ApiServer.views.getDisplays`

   * - Meals
     - GET
     - /api/meals
     - :ref:`Get Meals <getMeals>`
     - :py:func:`ApiServer.views.getMeals`

   * - Profs Absent
     - GET
     - /api/profsAbs
     - :ref:`Get Profs Abs <getProfsAbs>`
     - :py:func:`ApiServer.views.getProfsAbs`

   * - Post Vote
     - GET
     - /api/postVote
     - :ref:`Post Vote <postVote>`
     - :py:func:`ApiServer.views.postVote`

   * - Get Tweets
     - GET
     - /api/tweets
     - :ref:`Get Tweets <getTweets>`
     - :py:func:`ApiServer.views.getTweets`

   * - Get Meteo
     - GET
     - /api/meteo
     - :ref:`Get Meteo <getMeteo>`
     - :py:func:`ApiServer.views.getMeteo`

....

.. _getArticles:

Articles
------------

Récupère les articles visibles et les renvoie en JSON

Fonction associée : :py:func:`ApiServer.views.getArticles`

.. rubric:: Exemple :

``GET /api/articles``

.. rubric:: Retourne :

.. code-block:: JSON

	[
		{
			"title": "Mon bel article",
			"article": "Lorem ipsum blabla il est joli l'article pas vrai",
			"image": "Articles/IMG_5532_rTKf30T.png",
			"date_creation": "2022-01-17",
			"author": {
				"first_name": "Elo",
				"last_name": "Rap"
			},
			"date_last_modif": "2022-01-07"
		}
	]

....

.. _getInfos:

Informations
----------------

Récupère les informations visibles et les renvoie en JSON

Fonction associée : :py:func:`ApiServer.views.getInfos`

.. rubric:: Exemple :

``GET /api/infos``

.. rubric:: Retourne :

.. code-block:: JSON

	[
		{
			"message": "Internat fermé jusque nouvel ordre !",
			"type": {
				"id": 1,
				"name": "Important"
			},
			"date_creation": "2022-01-22",
			"author": {
				"first_name": "Elo",
				"last_name": "Rap"
			}
		}
	]

.. rubric:: Type d'informations:

.. list-table:: Tableau des différents types d'informations possibles
	:widths: 10 20 70
	:header-rows: 1

	* - ID
	  - Nom
	  - Comportement

	* - 1
	  - Important
	  - Texte en rouge sur les écrans

	* - 2
	  - Lambda
	  - Aucun comportement

....

.. _getSurveys:

Surveys
-------

Récupère les sondages visibles, avec les réponses associées et les renvoie en
JSON

Fonction associée : :py:func:`ApiServer.views.getSurveys`

.. rubric:: Exemple :

``GET /api/sondages``

.. rubric:: Retourne :

.. code-block:: JSON

	[
		{
			"id": 1,
			"author": 1,
			"subject": "Combat de MMA entre le proviseur et les AED",
			"date_creation": "2022-01-22",
			"date_end": "2022-02-06",
			"answers": [
				{
					"id": 1,
					"text": "Pour"
				},
				{
					"id": 2,
					"text": "Contre"
				}
			]
		}
	]

....

.. _getDisplays:

Displays
--------

Récupère l'écran et la page associée au paramètre code_name dans l'url 
de la requêtes et retourne les infos sous format JSON.

Fonction associée : :py:func:`ApiServer.views.getDisplays`

.. rubric:: Paramètres

.. list-table:: Tableau des paramètres possibles de l'url
    :widths: 34 33 33
    :header-rows: 1

    * - Nom
      - Type
      - Exemple de valeur

    * - code_name
      - str
      - viescolaire

.. rubric:: Exemple :

``GET /api/displays?code_name=viescolaire``

.. rubric:: Retourne :

.. code-block:: JSON

	[
		{
			"code_name": "viescolaire",
			"name": "Vie scolaire Bat C",
			"page": "Article + Profs abs + Agenda + Twitter"
		}
	]

....

.. _getMeals:

Meals
-----

Récupère le menu correpondant au paramètre date et retourne ses infos sous 
format JSON

Fonction associée : :py:func:`ApiServer.views.getMeals`

.. rubric:: Paramètres

.. list-table:: Tableau des paramètres possibles de l'url
    :widths: 34 33 33
    :header-rows: 1

    * - Nom
      - Type
      - Exemple de valeur

    * - date
      - str
      - 2022-01-19

.. rubric:: Exemple :

``GET /api/meals?date=2022-01-19``

.. rubric:: Retourne :

.. code-block:: JSON

	[
		{
			"date": "2022-01-19",
			"is_midday": true,
			"meal": {
				"1": [
					"Pâté en croûte ",
					"Salade verte oignons frits"
				],
				"2": [
					"Poisson pané ",
					"Côte d'agneau"
				],
				"3": [
					"Légumes grillés ",
					"Gratin dauphinois"
				],
				"4": [
					"eau"
				],
				"5": [
					"Fromage",
					"Yaourt"
				],
				"6": [
					"Fruit de saison",
					"Mousse chocolat ",
					"Ananas chantilly"
				]
			}
		},
	]

....

.. _getProfsAbs:

Profs Abs
-------------

Récupère les profs absent correpondant à la date d'aujourd'hui et retourne 
les infos sous format JSON

Fonction associée : :py:func:`ApiServer.views.getProfsAbs`

.. rubric:: Exemple :

``GET /api/profsAbs``

.. rubric:: Retourne :

.. code-block:: JSON

  [
    {
      "prof": "JESUS R.",
      "debut": "2022-01-19T21:15:25Z",
      "fin": "2022-01-19T23:15:35Z"
    }
  ]

....

.. _postVote:

Post Votes
----------

Poste le vote d'un utilisateur dans la DB à l'aide de l'username du password
et de l'id du vote

Retourne le status de la requête, si tout s'est bien passé ou non

Fonction associée : :py:func:`ApiServer.views.postVote`

.. rubric:: Paramètres

.. list-table:: Tableau des paramètres possibles de l'url
    :widths: 34 33 33
    :header-rows: 1

    * - Nom
      - Type
      - Exemple de valeur

    * - username
      - str
      - EloRap

    * - password
      - str
      - 123

    * - vote
      - int
      - 1

.. rubric:: Exemple :

``GET /api/postVote?vote=1&username=EloRap&password=123``

.. rubric:: Retourne :

.. code-block:: JSON

  [
      {
          "code": 200
          "message": ""
      }
  ]

.. rubric:: Code :

.. list-table:: Tableau des codes / messages possibles renvoyés
    :widths: 25 25 50
    :header-rows: 1

    * - Code
      - Message
      - Explication

    * - 200
      - 
      - Tout à bien fonctionné, le vote est posté

    * - 400
      - Il manque une information ! (soit vote, soit identifiants)
      - Une des informations est manquante dans la requête

    * - 403
      - Les identifiants sont invalides
      - Le couple username/password ne correspondent à aucun user dans la DB

    * - 404
      - Aucun sondage en cours
      - Aucun sondage n'est en cours

    * - 404
      - Mauvaise réponse
      - La réponse du vote donné n'existe pas / n'est pas trouvé dans la DB

....

.. _getTweets:

Tweets
----------

Récupère les 5 derniers tweets du lycée bourdelle et les retourne sous format 
JSON

Fonction associée : :py:func:`ApiServer.views.getTweets`

.. rubric:: Exemple :

``GET /api/tweets``

.. rubric:: Retourne :

.. code-block:: JSON

	{
		"data": [
			{
				"text": "ERASMUS avec les collèges @Col_Despeyrous ...",
				"created_at": "2022-01-21T09:47:27Z"
			},
			{
				"text": "ERASMUS+ LP BOURDELLE: signatures des con ...",
				"created_at": "2022-01-13T10:26:51Z"
			},
			{
				"text": "09/11/21 Les Term STL @LyceeBourdelle au m...",
				"created_at": "2022-01-11T08:13:50Z"
			},
			{
				"text": "ORIENTATION AMBITIEUSE @LyceeBourdelle : p...",
				"created_at": "2021-12-17T16:36:49Z"
			},
			{
				"text": "ERASMUS +@LyceeBourdelle : voyage préparat...",
				"created_at": "2021-12-17T16:11:51Z"
			}
		],
		"meta": {
			"oldest_id": "1471875800865689601",
			"newest_id": "1484462637899526147",
			"result_count": 5
		}
	}

....

.. _getMeteo:

Météo
----------

Renvoie la météo du jour avec les prévisions sur 2 jours sour format JSON

Voir `l'api de OpenWeatherMap <https://openweathermap.org/api/one-call-api>`_ 
pour plus d'infos sur la data renvoyée

Fonction associée : :py:func:`ApiServer.views.getMeteo`

.. rubric:: Exemple :

``GET /api/tweets``

.. rubric:: Retourne :

.. warning::
	Toutes les informations transmises par ``/api/meteo`` ne sont pas dans cet exemple car sinon
	l'exemple serait beaucoup trop long et peu utile. Donc, se trouve dans cet exemple,
	seules les informations que le projet utilise ou jugées utiles.

.. code-block:: JSON
	:tab-width: 4

	{
		"hourly": [
			{
				"dt": 1642878000,
				"temp": 3.47,
				"feels_like": 3.47,
				"weather": [
					{
						"id": 800,
						"main": "Clear",
						"description": "clear sky",
						"icon": "01n"
					}
				],
			},
		],
		"today": {
			"dt": 1642852800,
			"temp": {
				"day": 5.78,
				"min": -0.33,
				"max": 6.83,
				"night": 2.47,
				"eve": 3.33,
				"morn": -0.33
			},
			"feels_like": {
				"day": 4.4,
				"night": 2.47,
				"eve": 3.33,
				"morn": -0.33
			},
			"weather": [
				{
					"id": 800,
					"main": "Clear",
					"description": "clear sky",
					"icon": "01d"
				}
			],
		}
	}
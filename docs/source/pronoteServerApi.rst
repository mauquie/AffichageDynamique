Pronote Server API End points
=============================

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

   * - Menus
     - GET
     - /menus
     - :ref:`Get Menus <getmenus>`
     - :js:func:`getMenus`

   * - Emploi du temps
     - GET
     - /edt
     - :ref:`Get Emploi du temps <getedt>`
     - :js:func:`getEdt`

....

.. _getmenus:

Menus
-----

Récupère les menus à une date donnée et les renvoie en JSON

Fonction associée : :js:func:`getMenus`

.. rubric:: Exemple :

``GET /menus``

.. rubric:: Retourne :

.. code-block:: JSON

  {
    "data": [
      {
        "date": "2022-01-18T23:00:00.000Z",
        "meals": [
          [
            [
              {
                "name": "Pâté en croûte ",
                "labels": []
              },
              {
                "name": "Salade verte oignons frits",
                "labels": []
              }
            ],
            [
              {
                "name": "Poisson pané ",
                "labels": []
              },
              {
                "name": "Côte d'agneau",
                "labels": []
              }
            ],
            [
              {
                "name": "Légumes grillés ",
                "labels": []
              },
              {
                "name": "Gratin dauphinois",
                "labels": []
              }
            ],
            [
              {
                "name": "eau",
                "labels": []
              }
            ],
            [
              {
                "name": "Fromage",
                "labels": []
              },
              {
                "name": "Yaourt",
                "labels": []
              }
            ],
            [
              {
                "name": "Fruit de saison",
                "labels": []
              },
              {
                "name": "Mousse chocolat ",
                "labels": []
              },
              {
                "name": "Ananas chantilly",
                "labels": []
              }
            ]
          ],
        ]
      }
    ]
  }

....

.. _getedt:

Emploi du temps
---------------

Récupère l'emploi du temps à une date donnée et le renvoie en JSON

Fonction associée : :js:func:`getEdt`

.. rubric:: Exemple :

``GET /edt``

.. rubric:: Retourne :

.. code-block:: JSON

  {
    "data": [
      {
        "id": "17ff4dber7fd5d76",
        "from": "2022-01-19T07:00:00.000Z",
        "to": "2022-01-19T08:00:00.000Z",
        "isDetention": false,
        "remoteLesson": false,
        "hasDuplicate": false,
        "isAway": false,
        "isCancelled": false,
        "color": "#C0C0C0",
        "subject": "MATHS EXPERTES",
        "teacher": "ABRAHAM S.",
        "room": "B214"
      },
      {
        "id": "6d47cdc9dta132c",
        "from": "2022-01-19T08:00:00.000Z",
        "to": "2022-01-19T09:00:00.000Z",
        "isDetention": false,
        "remoteLesson": false,
        "hasDuplicate": false,
        "isAway": false,
        "isCancelled": false,
        "color": "#6ACAF2",
        "subject": "ANGLAIS LV1",
        "teacher": "NICEOREOL L.",
        "room": "C285 STMG"
      },
      {
        "id": "90a1cd9bc84b4po5",
        "from": "2022-01-19T09:00:00.000Z",
        "to": "2022-01-19T10:00:00.000Z",
        "isDetention": false,
        "remoteLesson": false,
        "hasDuplicate": false,
        "isAway": false,
        "isCancelled": false,
        "color": "#A2C62B",
        "subject": "HISTOIRE-GÉOGRAPHIE LGT",
        "teacher": "MACARON C.",
        "room": "C22 LV"
      },
      {
        "id": "6b9613a28d9fd403",
        "from": "2022-01-19T10:00:00.000Z",
        "to": "2022-01-19T11:00:00.000Z",
        "isDetention": false,
        "remoteLesson": false,
        "hasDuplicate": false,
        "isAway": false,
        "isCancelled": false,
        "color": "#80FFFF",
        "subject": "PHILOSOPHIE",
        "teacher": "SPAGHETTIS M.",
        "room": "T 102"
      }
    ]
  }
Pronote Server Fonctions
========================


.. js:function:: getSession()
  
  Créer la session pronote nécessaire pour récupérer ces données

  :returns: La session pronote
  :rtype: Session

....

.. js:function:: getMenus(session, date)

  Récupère les menus à une date donnée

  :param session: La session Pronote actuelle
  :type session: Session
  :param date: La date à laquelle on veut récupérer les données
  :type date: Date, optionnel

  :returns: La liste des menus à la date demandée
  :rtype: List

....

.. js:function:: getEdt(session, date)

  Récupère l'emploi du temps à une date donnée

  :param session: La session Pronote actuelle
  :type session: Session
  :param date: La date à laquelle on veut récupérer les données
  :type date: Date, optionnel

  :returns: La liste des cours de la date demandée
  :rtype: List

....

.. js:function:: gestionServeur(req, res, session)

  Gère les requetes sur le serveur, elle s'occupe de renvoyer les bonnes
  informations venant de la bonne url.

  Description des urls possibles :doc:`ici<pronoteServerApi>`

  :param req: La requête transmise par ``http.createServer()``
  :param res: La réponse à renvoyer à l'user, venant aussi de ``http.createServer()``
  :param session: La session Pronote actuelle
  :type session: Session

....

.. js:function:: generateDate()

  Génère un string contenant la date et l'heure au moment précis où 
  la fonction est exécutée

  :returns: Date sous le format ``[AAAA:MM:JJ HH:MM:SS]``
  :rtype: str

.... 

.. js:function:: gestionError(err, res)

  Gère les erreurs quand elle arrive, c'est à dire les notifie dans la
  console, redémarre la connexion avec pronote si nécessaire et renvoie 
  une liste vide de donnée

  :param err: Erreur générée par un ``.catch()``
  :param res: La réponse à renvoyer à l'user, venant de ``http.createServer()``

....

.. js:function:: loadSession()

  Charge le serveur sur le port 5000 une fois la connexion avec pronote réussi
"""
Gère toutes les vues correspondantes à l'api utilisée par les écrans pour
rafraichir les informations à afficher
"""

from django.http import JsonResponse
from .meteo import MeteoGetter

from django.core.handlers.wsgi import WSGIRequest
from django.db.models.query import QuerySet
from .twitter import getLastTweets
from .models import Articles, Informations, Screens, Meals, Absents, Surveys, Answers, Votes
from django.contrib.auth import authenticate
import datetime
from .pronote import refreshMenus, refreshProfs
import pytz
from AffichageDynamique import settings

meteoGetter = MeteoGetter()

def hideExpiredObjects(query: QuerySet):
    """
    Depuis une liste d'objets Django quelconque venant de la DB avec les
    colonnes date_end et shown, la fonction cache tous les objets ayant 
    un date_end plus petite que la date d'aujourd'hui

    Args:
        query (QuerySet): Liste d'objets Django à traiter
    """
    # Récupération de la date d'hier
    date = datetime.date.today()
    date = date.replace(day = date.day - 1)

    # Modification de tous les objets aillant une date d'expiration plus 
    # petite ou égale à hier
    expiredObjects = query.filter(date_end__lte = date)

    # Pour tous ces objets, on les cache
    for entry in expiredObjects:
        entry.is_shown = False
        entry.save()

def getArticles(request: WSGIRequest) -> JsonResponse:
    """
    Récupère les articles visibles et retourne la requête en JSONResponse

    Args:
        request (WSGIRequest): Requête Django

    Returns:
        JSONResponse: Requête Django correspondante au renvoie d'un fichier JSON

    Example:
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
        
    """
    # Récupération de tous les articles
    query = Articles.objects.all()
    
    # On cache tous les articles passés 
    hideExpiredObjects(query)    

    # On récupère tous les articles affichés
    query = query.filter(is_shown = True)

    articlesList = list()

    # Formatage des données à renvoyer 
    for entry in query:
        json = {
            "title": entry.title,
            "article": entry.content,
            "image": str(entry.image),
            "date_creation": entry.date_creation,
            "author": {
                "first_name": entry.author.first_name,
                "last_name": entry.author.last_name
            },
            "date_last_modif": entry.date_last_modif,
        }

        articlesList.append(json)

    return JsonResponse(articlesList, safe=False)

def getInfos(request: WSGIRequest) -> JsonResponse:
    """
    Récupère les informations visibles et les retourne sous format JSON.

    Args:
        request (WSGIRequest): Requête Django

    Returns:
        JSONResponse: Requête Django correspondante au renvoie d'un fichier JSON

    Example:
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
            
    """
    # Récupération de toutes les informations
    query = Informations.objects.all()

    # On cache toutes les informations passées
    hideExpiredObjects(query)

    # Récupération des informations toujours à l'affiche après le "tri" de 
    # hideExpiredObjects
    query = query.filter(is_shown = True)

    infoList = list()

    # Formatage des données
    for entry in query:
        json = {
            "message": entry.message,
            "type": {
                "id": entry.type.id,
                "name": entry.type.name
            },
            "date_creation": entry.date_creation,
            "author": {
                "first_name": entry.author.first_name,
                "last_name": entry.author.last_name
            }

        }

        infoList.append(json)

    return JsonResponse(infoList, safe=False)

def getSurveys(request: WSGIRequest) -> JsonResponse:
    """
    Récupère les sondages visibles, avec les réponses associées et les retourne 
    sous format JSON.

    Args:
        request (WSGIRequest): Requête Django

    Returns:
        JSONResponse: Requête Django correspondante au renvoie d'un fichier JSON

    Example:
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
    """
    
    # Récupération de tous les sondages
    query = Surveys.objects.all()

    # On cache tous les sondages passés
    hideExpiredObjects(query)

    # Récupération des sondages qui ont survécus au tri 
    query = query.filter(is_shown = True)

    surveyList = list()

    # Formatage des données
    for entry in query:
        answers = Answers.objects.filter(survey=entry.id)

        json = {
            "id": entry.id,
            "author": entry.author.id,
            "subject": entry.subject,
            "date_creation": entry.date_creation,
            "date_end": entry.date_end,
            "answers": [
                {"id": answer.id, "text": answer.answer} 
                for answer in answers
                ]
        }

        surveyList.append(json)

    return JsonResponse(surveyList, safe=False)

def getDisplays(request: WSGIRequest) -> JsonResponse:
    """
    Récupère l'écran et la page associée au paramètre code_name dans l'url 
    de la requêtes et retourne les infos sous format JSON.

    Args:
        request (WSGIRequest): Requête Django

        code_name (str): Paramètre passé à la requête, codename de l'écran que l'user
            veut obtenir les infos

    Returns:
        JSONResponse: Requête Django correspondante au renvoie d'un fichier JSON

    Example:
        .. code-block:: JSON

            [
                {
                    "code_name": "viescolaire",
                    "name": "Vie scolaire Bat C",
                    "page": "Article + Profs abs + Agenda + Twitter"
                }
            ]
            
    """
    # Récupération de l'ecran aillant le code_name égal au parametre de la 
    # requete
    query = Screens.objects.filter(code_name=request.GET.get("code_name"))

    infoList = []

    for entry in query:
        if entry.page: # Si on a une page configurée pour l'écran
            page = entry.page.description

        else: 
            # Si on n'a pas de page configurée ou qu'on a pas trouvé 
            # l'écran correspondant au code_name
            page = "Base"

        json = {
            "code_name": entry.code_name,
            "name": entry.name,
            "page": page
        }
        infoList.append(json)
    
    return JsonResponse(infoList, safe=False)

def getMeals(request: WSGIRequest) -> JsonResponse:
    """
    Récupère le menu correpondant au paramètre date et retourne ses infos sous 
    format JSON

    Args:
        request (WSGIRequest): Requête Django
        date (str): Paramètre passé à la requête, il faut qu'elle est la forme
            2022-01-19

    Returns:
        JSONResponse: Requête Django correspondante au renvoie d'un fichier JSON

    Example:
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
    """
    refreshMenus()

    # Récupération du repas dans la bdd à la date donnée
    query = Meals.objects.filter(date=request.GET.get("date"))

    infoList = []

    # Pour chaque repas du jour
    for entry in query:
        meal = {}
        
        # Création de 6 listes qui vont contenir respenctivement une partie du 
        # repas
        # (Une liste pour les aliments de l'entrée, une pour les viandes, les 
        # desserts etc)
        for x in range(1, 7):
            meal[x] = []

        # Pour chaque aliment du repas, on ajoute l'aliment à la liste 
        # correspondant à sa partie du repas
        for food in entry.to_eat.all():
            meal[food.meal_part.id].append(food.name)

        # On formate les données à renvoyer  
        json = {
            "date": request.GET.get("date"),
            "is_midday": entry.is_midday,
            "meal": meal
        }

        # On ajoute le dictionnaire à la liste qui va contenir tous 
        # les repas différents 
        infoList.append(json)
    
    return JsonResponse(infoList, safe=False)

def getProfsAbs(request: WSGIRequest) -> JsonResponse:
    """
    Récupère les profs absent correpondant à la date d'aujourd'hui et retourne 
    les infos sous format JSON

    Si on est en mode DEBUG=True, alors il prendra 10 profs abs au hasard pour les
    test

    Args:
        request (WSGIRequest): Requête Django

    Returns:
        JSONResponse: Requête Django correspondante au renvoie d'un fichier JSON

    Example:
        .. code-block:: JSON

            [
                {
                    "prof": "JESUS R.",
                    "debut": "2022-01-19T21:15:25Z",
                    "fin": "2022-01-19T23:15:35Z"
                }
            ]
    """

    refreshProfs()

    query = None

    if settings.DEBUG:
        query = Absents.objects.all()[:10]
    else:
        offset = datetime.datetime.now(pytz.timezone('Europe/Paris'))
        offset = offset.strftime('%z')[2]
        offset = int(offset)*3600*24

        # Calcul des dates d'aujourd'hui et demain
        dateToday = datetime.datetime.now(tz = datetime.timezone.utc)
        dateToday.replace(hour = 0, minute = 0, second = 0)

        dateTomorrow = datetime.datetime.now(tz = datetime.timezone.utc).timestamp()
        dateTomorrow = datetime.datetime.utcfromtimestamp(dateTomorrow + offset)
        dateTomorrow = dateTomorrow.replace(hour = 0, minute = 0, second = 0, 
            tzinfo=datetime.timezone.utc)

        # On récupère tous les profs absents depuis aujourd'hui ou avant et jusqu'à 
        # minimum aujourd'hui ou plus
        query = Absents.objects.filter(date_start__lte=dateTomorrow, date_end__gte=dateToday)
    
    infoList = []

    # Pour chaque prof
    for entry in query:
        json = {
            "prof" : entry.teacher.name,
            "debut" : entry.date_start,
            "fin": entry.date_end,
        }

        infoList.append(json)

    return JsonResponse(infoList, safe=False)

def postVote(request: WSGIRequest) -> JsonResponse:
    """
    Poste le vote d'un utilisateur dans la DB à l'aide de l'username du password
    et de l'id du vote (respectivement les paramètres username, password, vote)
    Retourne le status de la requête, si tout s'est bien passé ou non

    Args:
        request (WSGIRequest): Requête Django
        username (str): Paramètre passé à la requête, nom d'utilisateur du votant
        password (str): Paramètre passé à la requête, mot de passe du votant
        vote (int): Paramètre passé à la requête, id de la réponse du votant

    Returns:
        JSONResponse: Requête Django correspondante au renvoie d'un fichier JSON

    Example:
        .. code-block:: JSON

            [
                {
                    "code": 200,
                    "message": ""
                }
            ]
    """
    if request.method == "GET":
        # Récupération des données transmises
        username = request.GET.get("username", "")
        password = request.GET.get("password", "")
        answerVoted = request.GET.get("vote", "")

        # Vérification qu'il y ait tous les champs demandés
        if not answerVoted or not username or not password:
            return JsonResponse(
                {
                    "code": 400,
                    "message": "Il manque une information ! (soit vote, soit identifiants)"
                }
            )

        # Vérification que le compte donné existe
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # On fait voter l'utilisateur

            # Vérification qu'il y a bien un sondage en cours
            surveys = Surveys.objects.filter(is_shown = True)
            if len(surveys) < 1:
                return JsonResponse(
                    {
                        "code": 404, 
                        "message": "Aucun sondage en cours"
                    }
                )

            else:
                # On prend que le premier sondage affiché s'il y en a
                #  plusieurs (ne doit PAS arriver)
                survey = surveys[0] 

                # Vérification que l'utilisateur donné n'a pas déjà voté
                votes = Votes.objects.filter(author=user.id, survey=survey.id)
                if len(votes) > 0:
                    return JsonResponse({"code": 403, "message": "A déjà voté"})
                

                # Récupération des reponses possibles au sondage
                answersSurvey = Answers.objects.filter(survey = survey.id)

                # Récupération de la reponse choisi parmi elles
                answer = answersSurvey.filter(pk = answerVoted)
                
                # Vériication qu'il ait donné une réponse possible
                if len(answer) == 0:
                    return JsonResponse(
                        {
                            "code": 404, 
                            "message": "Mauvaise réponse"
                        }
                    )

                else:
                    # Enregistrement du vote
                    vote = Votes()
                    vote.author = user
                    vote.answer = answer[0]
                    vote.survey = survey

                    vote.save()

                    return JsonResponse({"code": 200})

        else:
            return JsonResponse(
                {
                    "code": 403,
                    "message": "Les identifiants sont invalides"
                }
            )

def getTweets(request: WSGIRequest) -> JsonResponse:
    """
    Renvoie les 5 derniers tweets postés du compte LycéeBourdelle

    Args:
        request (WSGIRequest): Requête Django

    Returns:
        JSONResponse: Requête Django correspondante au renvoie d'un fichier JSON

    Example:
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
    """
    tweets = getLastTweets()

    return JsonResponse(tweets)

def getMeteo(request: WSGIRequest) -> JsonResponse:
    """
    Renvoie la météo du jour avec les prévisions sur 2 jours sour format JSON

    Voir `l'api de OpenWeatherMap <https://openweathermap.org/api/one-call-api>`_ 
    pour plus d'infos sur la data renvoyée

    Args:
        request (WSGIRequest): Requête Django

    Returns:
        JSONResponse: Requête Django correspondante au renvoie d'un fichier JSON

    Example
        .. code-block:: JSON

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
    """
    meteo = meteoGetter.getMeteoData()

    return JsonResponse(meteo)
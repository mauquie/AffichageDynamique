from django.shortcuts import render
from django.http import JsonResponse
from AffichageDynamiqueServer.ApiServer.meteo import MeteoGetter

from ApiServer.twitter import getLastTweets
from .models import Articles, Informations, Screens, Meals, Absents, Surveys, Answers, Votes
from django.contrib.auth import authenticate
import datetime
from .pronote import refreshMenus, refreshProfs
import pytz

meteoGetter = MeteoGetter()

def hideExpiredObjects(query):
    # Récupération de la date d'hier
    date = datetime.date.today()
    date = date.replace(day = date.day - 1)

    # Modification de tous les objets aillant une date d'expiration plus petite ou égale à hier
    expiredObjects = query.filter(date_end__lte = date)

    # Pour tous ces objets, on les cache
    for entry in expiredObjects:
        entry.is_shown = False
        entry.save()

#  Récupère les articles visibles et les retourne sous format JSON.
def getArticles(request)->JsonResponse:
    #  Récupération de tous les articles
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
            "last_edit_by": {
                "first_name": entry.author.first_name,
                "last_name": entry.author.last_name
            }

        }

        articlesList.append(json)

    return JsonResponse(articlesList, safe=False)

#  Récupère les informations visibles et les retourne sous format JSON.
def getInfos(request)->JsonResponse:
    # Récupération de toutes les informations
    query = Informations.objects.all()

    # On cache toutes les informations passées
    hideExpiredObjects(query)

    # Récupération des informations toujours à l'affiche après le "tri" de hideExpiredObjects
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

#  Récupère les sondages visibles et les retourne sous format JSON.
def getSurveys(request)->JsonResponse:
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
            "answers": [{"id": answer.id, "text": answer.answer} for answer in answers]
        }

        surveyList.append(json)

    return JsonResponse(surveyList, safe=False)

# Récupère l'écran correspondant au paramètre code_name et retourne ses infos sous format JSON
def getDisplays(request)->JsonResponse:
    # Récupération de l'ecran aillant le code_name égal au parametre de la requete
    query = Screens.objects.filter(code_name=request.GET.get("code_name"))

    infoList = []

    for entry in query:
        if entry.page: # Si on a une page configurée pour l'écran
            page = entry.page.description

        else: # Si on n'a pas de page configurée ou qu'on a pas trouvé l'écran correspondant au code_name
            page = "Base"

        json = {
            "code_name": entry.code_name,
            "name": entry.name,
            "page": page
        }
        infoList.append(json)
    
    return JsonResponse(infoList, safe=False)

# Récupère le menu correpondant au paramètre date et retourne ses infos sous format JSON
def getMenus(request)->JsonResponse:
    refreshMenus()

    # Récupération du repas dans la bdd à la date donnée
    query = Meals.objects.filter(date=request.GET.get("date"))

    infoList = []

    # Pour chaque repas du jour
    for entry in query:
        meal = {}
        
        # Création de 6 listes qui vont contenir respenctivement une partie du repas
        # (Une liste pour les aliments de l'entrée, une pour les viandes, les desserts etc)
        for x in range(1, 7):
            meal[x] = []

        # Pour chaque aliment du repas, on ajoute l'aliment à la liste correspondant à sa partie du repas
        for food in entry.to_eat.all():
            meal[food.to_eat.id].append(food.name)

        # On formate les données à renvoyer  
        json = {
            "date": request.GET.get("date"),
            "is_midday": entry.is_midday,
            "meal": meal
        }

        # On ajoute le dictionnaire à la liste qui va contenir tous les repas différents 
        infoList.append(json)
    
    return JsonResponse(infoList, safe=False)

def getProfsAbs(request):
    refreshProfs()

    offset = int(datetime.datetime.now(pytz.timezone('Europe/Paris')).strftime('%z')[2])*3600*24

    # Calcul des dates d'aujourd'hui et demain
    dateToday = datetime.datetime.now(tz = datetime.timezone.utc).replace(hour = 0, minute = 0, second = 0)
    dateTomorrow = datetime.datetime.now(tz = datetime.timezone.utc)

    dateTomorrow = datetime.datetime.utcfromtimestamp(dateTomorrow.timestamp() + offset).replace(hour = 0, minute = 0, second = 0, tzinfo=datetime.timezone.utc)

    # On récupère tous les profs absents depuis aujourd'hui ou avant et jusqu'à minimum aujourd'hui ou plus
    peretty = Absents.objects.filter(teacher=1)
    query = Absents.objects.filter(date_start__lte=dateTomorrow, date_end__gte=dateToday)
    print(query)
    infoList = []

    # Poru chaque prof
    for entry in query:
        json = {
            "prof" : entry.teacher.name,
            "debut" : entry.date_start,
            "fin": entry.date_end,
        }

        infoList.append(json)

    return JsonResponse(infoList, safe=False)

def postVote(request):
    if request.method == "GET":
        # Récupération des données transmises
        username = request.GET.get("username", "")
        password = request.GET.get("password", "")
        answerVoted = request.GET.get("vote", "")

        # Vérification qu'il y ait tous les champs demandés
        if not answerVoted or not username or not password:
            return JsonResponse({"code": 400,"message": "Il manque une information ! (soit vote, soit identifiants)"})

        # Vérification que le compte donné existe
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # On fait voter l'utilisateur

            # Vérification qu'il y a bien un sondage en cours
            surveys = Surveys.objects.filter(is_shown = True)
            if len(survey) < 1:
                return JsonResponse({"code": 404, "message": "Aucun sondage en cours"})

            else:
                survey = survey[0] # On prend que le premier sondage affiché s'il y en à plusieurs (ne doit PAS arriver)

                # Vérification que l'utilisateur donné n'a pas déjà voté
                votes = Votes.objects.filter(auteur=user.id, sondage=sondage.id)
                if len(votes) > 0:
                    return JsonResponse({"code": 403, "message": "A déjà voté"})
                

                # Récupération des reponses possibles au sondage
                answersSurvey = Reponse.objects.filter(sondage = sondage.id)

                # Récupération de la reponse choisi parmi elles
                answer = answersSurvey.filter(pk = answerVoted)
                
                # Vériication qu'il ait donné une réponse possible
                if len(answer) == 0:
                    return JsonResponse({"code": 404, "message": "Mauvaise réponse"})

                else:
                    # Enregistrement du vote
                    vote = Votes()
                    vote.author = user
                    vote.answer = answer[0]
                    vote.survey = survey

                    vote.save()

                    return JsonResponse({"code": 200})

        else:
            return JsonResponse({"code": 403,"message": "Les identifiants sont invalides"})

def getTweets(request):
    # Vue renvoyant les 5 derniers tweets postés
    tweets = getLastTweets()

    return JsonResponse(tweets)

def getMeteo(request):
    meteo = meteoGetter.getMeteoData()

    return JsonResponse(meteo)
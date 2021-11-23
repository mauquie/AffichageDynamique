from django.shortcuts import render
from django.http import JsonResponse
from .models import Article, Info, SondageAdmin, Survey, Display, Repas, ProfAbsent, Sondage, Reponse, Vote
from django.contrib.auth import authenticate
import datetime
from .pronote import refreshMenus, refreshProfs

def hideExpiredObjects(query):
    #Récupération de la date d'hier
    date = datetime.date.today()
    date = date.replace(day = date.day - 1)

    #Modification de tous les objets aillant une date d'expiration plus petite ou égale à hier
    expiredObjects = query.filter(expiration_date__lte = date)

    #Pour tous ces objets, on les cache
    for entry in expiredObjects:
        entry.is_shown = False
        entry.save()

# Récupère les articles visibles et les retourne sous format JSON.
def getArticles(request)->JsonResponse:
    # Récupération de tous les articles
    query = Article.objects.all()
    
    #On cache tous les articles passés 
    hideExpiredObjects(query)    

    #On récupère tous les articles affichés
    query = query.filter(is_shown = True)

    articleList = list()

    #Formatage des données à renvoyer 
    for entry in query:
        json = {
            "title": entry.title,
            "article": entry.article,
            "image": str(entry.image),
            "creation_date": entry.creation_date,
            "author": {
                "first_name": entry.author.first_name,
                "last_name": entry.author.last_name
            },
            "modification_date": entry.modification_date,
            "last_edit_by": {
                "first_name": entry.author.first_name,
                "last_name": entry.author.last_name
            }

        }

        articleList.append(json)

    return JsonResponse(articleList, safe=False)

# Récupère les informations visibles et les retourne sous format JSON.
def getInfos(request)->JsonResponse:
    #Récupération de toutes les informations
    query = Info.objects.all()

    #On cache toutes les informations passées
    hideExpiredObjects(query)

    #Récupération des informations toujours à l'affiche après le "tri" de hideExpiredObjects
    query = query.filter(is_shown = True)

    infoList = list()

    #Formatage des données
    for entry in query:
        json = {
            "message": entry.message,
            "type": {
                "id": entry.type.id,
                "name": entry.type.name
            },
            "creation_date": entry.creation_date,
            "author": {
                "first_name": entry.author.first_name,
                "last_name": entry.author.last_name
            }

        }

        infoList.append(json)

    return JsonResponse(infoList, safe=False)

# Récupère les sondages visibles et les retourne sous format JSON.
def getSurveys(request)->JsonResponse:
    #Récupération de tous les sondages
    query = Survey.objects.all()

    #On cache tous les sondages passés
    hideExpiredObjects(query)

    #Récupération des sondages qui ont survécus au tri 
    query = query.filter(is_shown = True)

    surveyList = list()

    #Formatage des données
    for entry in query:
        json = {
            "description": entry.description,
            "link": entry.link,
            "creation_date": entry.creation_date,
            "author": {
                "first_name": entry.author.first_name,
                "last_name": entry.author.last_name
            }

        }

        surveyList.append(json)

    return JsonResponse(surveyList, safe=False)

#Récupère l'écran correspondant au paramètre code_name et retourne ses infos sous format JSON
def getDisplays(request)->JsonResponse:
    #Récupération de l'ecran aillant le code_name égal au parametre de la requete
    query = Display.objects.filter(code_name=request.GET.get("code_name"))

    infoList = []

    for entry in query:
        if entry.page: #Si on a une page configurée pour l'écran
            page = entry.page.description

        else: #Si on n'a pas de page configurée ou qu'on a pas trouvé l'écran correspondant au code_name
            page = "Base"

        json = {
            "code_name": entry.code_name,
            "name": entry.name,
            "page": page
        }
        infoList.append(json)
    
    return JsonResponse(infoList, safe=False)

#Récupère le menu correpondant au paramètre date et retourne ses infos sous format JSON
def getMenus(request)->JsonResponse:
    refreshMenus()

    #Récupération du repas dans la bdd à la date donnée
    query = Repas.objects.filter(date=request.GET.get("date"))

    infoList = []

    #Pour chaque repas du jour
    for entry in query:
        repas = {}
        
        #Création de 6 listes qui vont contenir respenctivement une partie du repas
        #(Une liste pour les aliments de l'entrée, une pour les viandes, les desserts etc)
        for x in range(1, 7):
            repas[x] = []

        #Pour chaque aliment du repas, on ajoute l'aliment à la liste correspondant à sa partie du repas
        for aliment in entry.aliments_du_repas.all():
            repas[aliment.partie_du_repas.id].append(aliment.name)

        #On formate les données à renvoyer  
        json = {
            "date": request.GET.get("date"),
            "midi": entry.repas_midi,
            "repas": repas
        }

        #On ajoute le dictionnaire à la liste qui va contenir tous les repas différents 
        infoList.append(json)
    
    return JsonResponse(infoList, safe=False)

def getProfsAbs(request):
    refreshProfs()

    #Calcul des dates d'aujourd'hui et demain
    dateToday = datetime.datetime.now(tz = datetime.timezone.utc).replace(hour = 0, minute = 0, second = 0)
    dateTomorrow = datetime.datetime.now(tz = datetime.timezone.utc).replace(hour = 0, minute = 0, second = 0)

    dateTomorrow = dateTomorrow.replace(day = dateTomorrow.day + 1)

    #On récupère tous les profs absents de la journée 
    query = ProfAbsent.objects.filter(debut__gte=dateToday, debut__lte=dateTomorrow)

    infoList = []

    #Poru chaque prof
    for entry in query:
        #Convertion des heures dans le bon fuseau horaire (Paris +2:00)
        debut = entry.debut.replace(hour = entry.debut.hour + 2)
        fin = entry.fin.replace(hour = entry.fin.hour + 2)

        json = {
            "prof" : entry.teacher,
            "debut" : debut,
            "fin": fin,
        }

        infoList.append(json)

    return JsonResponse(infoList, safe=False)

def postVote(request):
    if request.method == "GET":
        #Récupération des données transmises
        username = request.GET.get("username", "")
        password = request.GET.get("password", "")
        reponseVotee = request.GET.get("vote", "")

        #Vérification qu'il y ait tous les champs demandés
        if not reponseVotee or not username or not password:
            return JsonResponse({"code": 400,"message": "Il manque une information ! (soit vote, soit identifiants)"})

        #Vérification que le compte donné existe
        user = authenticate(request, username=username, password=password)
        if user is not None:
            #On fait voter l'utilisateur

            #Vérification qu'il y a bien un sondage en cours
            sondage = Sondage.objects.filter(est_affiche = True)
            if len(sondage) < 1:
                return JsonResponse({"code": 404, "message": "Aucun sondage en cours"})

            else:
                sondage = sondage[0] #On prend que le premier sondage affiché s'il y en à plusieurs (ne doit PAS arriver)

                #Vérification que l'utilisateur donné n'a pas déjà voté
                votes = Vote.objects.filter(auteur=user.id, sondage=sondage.id)
                if len(votes) > 0:
                    return JsonResponse({"code": 403, "message": "A déjà voté"})
                

                #Récupération des reponses possibles au sondage
                reponsesSondage = Reponse.objects.filter(sondage = sondage.id)

                #Récupération de la reponse choisi parmi elles
                reponse = reponsesSondage.filter(pk = reponseVotee)
                
                #Vériication qu'il ait donné une réponse possible
                if len(reponse) == 0:
                    return JsonResponse({"code": 404, "message": "Mauvaise réponse"})

                else:
                    #Enregistrement du vote
                    vote = Vote()
                    vote.auteur = user
                    vote.vote = reponse[0]
                    vote.sondage = sondage

                    vote.save()

                    return JsonResponse({"code": 200})

        else:
            return JsonResponse({"code": 403,"message": "Les identifiants sont invalides"})
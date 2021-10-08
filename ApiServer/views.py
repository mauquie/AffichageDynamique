from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
from .models import Article, Info, Survey, Display
import datetime

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
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
from .models import Article, Info, Survey, Display

# Récupère les articles visibles et les retourne sous format JSON.
def getArticles(request)->JsonResponse:
    query = Article.objects.filter(is_shown=True)
    
    [entry for entry in query]
    articleList = list()

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
    query = Info.objects.filter(is_shown=True)

    [entry for entry in query]
    infoList = list()

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
    query = Survey.objects.filter(is_shown=True)

    [entry for entry in query]
    surveyList = list()

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
    query = Display.objects.filter(code_name=request.GET.get("code_name"))

    infoList = []

    for entry in query:
        if entry.page:
            page = entry.page.description

        else:
            page = "Base"

        json = {
            "code_name": entry.code_name,
            "name": entry.name,
            "page": page
        }
        infoList.append(json)
    
    return JsonResponse(infoList, safe=False)
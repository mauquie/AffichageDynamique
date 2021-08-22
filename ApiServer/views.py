from django.shortcuts import render
from django.http import JsonResponse
from .models import Article

# Create your views here.
def index(request):
    return getArticles()

def getArticles()->JsonResponse:
    query = Article.objects.filter(is_shown=True)
    [entry for entry in query]
    list = {}
    for entry in query:
        json = {
            "title": entry.title,
            "article": entry.article,
            "image": entry.image,
            "creation_date": entry.creation_date,
            "expiration_date": entry.expiration_date,
            "author": entry.author,
            "modification_date": entry.modification_date,
            "last_edit_by": entry.last_edit_by
        }
        list.append(json)
    return JsonResponse(list)
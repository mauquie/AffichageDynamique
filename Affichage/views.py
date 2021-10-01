from django.shortcuts import render
from django.http import JsonResponse
from ApiServer.models import Article
from ApiServer.views import getArticles
from datetime import date
import json
# Create your views here.

def index(request):
    return JsonResponse({"text": "Page du premier écran !"})

def vieScolaire(request):
    data = getArticles(request)
    context = {"data" : data}
    return render(request, "Affichage/vieScolaire.html", context)
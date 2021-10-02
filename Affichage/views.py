from django.shortcuts import render
from django.http import JsonResponse
from ApiServer.models import Article, Display
from ApiServer.views import getArticles
from datetime import date
# Create your views here.

def index(request):
<<<<<<< HEAD
    return JsonResponse({"text": "Page du premier écran !"})
=======
    return JsonResponse({})
>>>>>>> 2bbef78a7b263c01e585fe65d3abba0ded2310a8

def affichageEcran(request):
    #Lien vers l'écran en cas d'erreurs
    path = "Affichage/base.html"

    #Récupération du paramètre nom pour connaitre l'écran que l'on veut afficher
    displayName = request.GET.get("name", "")

    #Si displayName est bien renseigné
    if displayName:
        #Recherche dans la bdd s'il y a un écran qui correspond au paramètre donné
        display = Display.objects.all().filter(code_name = displayName)
        
        #S'il y a bien un écran qui correspond au paramètre
        if len(display) > 0:
            #On récupère le nom du fichier associé à la page associé à l'écran s'il y en a un
            if display[0].page:
                path = "Affichage/" + display[0].page.filename

    return render(request, path)

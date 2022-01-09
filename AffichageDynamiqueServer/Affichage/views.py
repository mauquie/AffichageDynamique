from django.shortcuts import render
from django.http import JsonResponse
from ApiServer.models import Screens
from datetime import date
# Create your views here.

def index(request):
    return JsonResponse({})

def affichageEcran(request):
    #Lien vers l'écran en cas d'erreurs
    path = "Affichage/base.html"
    context = {"description": "Base"}

    #Récupération du paramètre nom pour connaitre l'écran que l'on veut afficher
    screenName = request.GET.get("name", "")

    #Si screenName est bien renseigné
    if screenName:
        #Recherche dans la bdd s'il y a un écran qui correspond au paramètre donné
        screens = Screens.objects.all().filter(code_name = screenName)
        
        #S'il y a bien un écran qui correspond au paramètre
        if len(screens) > 0:
            #On récupère le nom du fichier associé à la page associé à l'écran s'il y en a un
            if screens[0].page:
                path = "Affichage/" + screens[0].page.filename

                context = {"description": screens[0].page.description}
    return render(request, path, context)
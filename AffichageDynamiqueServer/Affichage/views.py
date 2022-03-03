"""
Gère toutes les vues correspondantes à l'affichage sur les écrans
"""

from django.http import HttpResponse
from django.shortcuts import render
from ApiServer.models import Screens
from django.core.handlers.wsgi import WSGIRequest
import AffichageDynamique.settings as settings

def affichageEcran(request: WSGIRequest) -> HttpResponse:
    """
    Rédirige l'user à l'écran demandé via le paramètre name

    Args:
        request (WSGIRequest): Requête Django
        name (str): Paramètre passé à la requête, nom de code de l'écran voulu,
            si trouvé alors il renvoie l'écran, si non alors il renvoie l'écran
            ``base``, celui par défaut.

    Returns:
        HttpResponse: Ecran correspondant à la demande
    """

    # Lien vers l'écran en cas d'erreurs
    path = "Affichage/base.html"
    context = {"description": "Base"}

    # Récupération du paramètre nom pour connaitre l'écran que l'on veut afficher
    screenName = request.GET.get("name", "")
    key = request.GET.get("k", "")

    # Si screenName est bien renseigné
    if screenName:
        # Recherche dans la bdd s'il y a un écran qui correspond au paramètre donné
        screens = Screens.objects.all().filter(code_name = screenName)
        
        # S'il y a bien un écran qui correspond au paramètre
        if len(screens) > 0:
            # Si on est en production et que la clé ne correspond pas
            # alors on refuse l'accés aux écrans
            if not settings.DEBUG and key != screens[0].uuid:
                return HttpResponse('Unauthorized', status=401)

            # On récupère le nom du fichier associé à la page associé à l'écran s'il y en a un
            if screens[0].page:
                path = "Affichage/" + screens[0].page.filename

                context = {"description": screens[0].page.description}

    return render(request, path, context)
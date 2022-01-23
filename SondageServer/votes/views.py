"""
Gère toutes les vues nécessaires pour le serveur Sondage
"""

from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect
import requests
import json

from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.

def successVote(request: WSGIRequest) -> HttpResponse:
    """
    Renvoie la page de succès

    Args:
        request (WSGIRequest): Requête Django

    Returns:
        HttpResponse: Page de succès
    """
    return render(request, "success.html")

def surveyExpired(request: WSGIRequest) -> HttpResponse:
    """
    Renvoie la page d'aucune sondage en cours

    Args:
        request (WSGIRequest): Requête Django

    Returns:
        HttpResponse: Page aucun sondage
    """
    return render(request, "expired.html")

def alreadyVoted(request: WSGIRequest) -> HttpResponse:
    """
    Renvoie la page du déjà voté

    Args:
        request (WSGIRequest): Requête Django

    Returns:
        HttpResponse: Page déjà voté
    """
    return render(request, "already.html")

def missingInfo(request: WSGIRequest) -> HttpResponse:
    """
    Page d'erreur infos manquantes

    Args:
        request (WSGIRequest): Requête Django

    Returns:
        HttpResponse: Page infos manquantes
    """
    return render(request, "missing.html")

def badId(request: WSGIRequest) -> HttpResponse:
    """
    Page d'erreur mauvaise reponse id

    Args:
        request (WSGIRequest): Requête Django

    Returns:
        HttpResponse: Page mauvaise reponse
    """
    return render(request, "bad.html")

def index(request: WSGIRequest) -> HttpResponse:
    """
    Page initiale de vote

    Args:
        request (WSGIRequest): Requête Django

    Returns:
        HttpResponse: Page de vote
    """
    url = requests.get('http://localhost:8000/api/sondages')
    data = json.loads(url.content)
    data = json.dumps(data)
    context = {
        "data" : data
    }
    return render(request, "index.html", context=context)

def postVote(request: WSGIRequest) -> HttpResponse:
    """
    Gère l'envoie des votes au serveur :ref:`affichage dynamique <affichagedynamique>`

    Args:
        request (WSGIRequest): Requête Django

    Returns:
        HttpResponse: Page de statut du vote
    """
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        vote = request.POST.get("vote")

        postVoteRequest = requests.request(method="get", url="http://localhost:8000/api/postVote?vote={}&username={}&password={}".format(vote, username, password))
        if postVoteRequest.json()["code"] == 400:
            return HttpResponseRedirect("/missing")
        elif postVoteRequest.json()["code"] == 403:
            if postVoteRequest.json()["message"] == "Les identifiants sont invalides":
                return HttpResponseRedirect("/bad")
            elif postVoteRequest.json()["message"] == "A déjà voté":
                return HttpResponseRedirect("/already")
        elif postVoteRequest.json()["code"] == 404:
            return HttpResponseRedirect("/expired")
        elif postVoteRequest.json()["code"] == 200:
            return HttpResponseRedirect("/success")

        else:
            print(postVoteRequest.json())

    else:
        return redirect("/")
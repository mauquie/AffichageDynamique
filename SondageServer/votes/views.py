from django.shortcuts import render, redirect
import requests
import json

from django.http import HttpResponseRedirect

# Create your views here.

def successVote(request):
    return render(request, "success.html")

def surveyExpired(request):
    return render(request, "expired.html")

def alreadyVoted(request):
    return render(request, "already.html")

def missingInfo(request):
    return render(request, "missing.html")

def index(request):
    url = requests.get('http://localhost:8000/api/sondages')
    data = json.loads(url.content)
    data = json.dumps(data)
    context = {
        "data" : data
    }
    return render(request, "index.html", context=context)

def postVote(request):
    '''
        Fonction gérant la connexion des utilisateurs
    '''
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        vote = request.POST.get("vote")

        postVoteRequest = requests.request(method="get", url="localhost:8000/api/postVote?vote={}&username={}&password={}".format(vote, username, password))
        if postVoteRequest.json()["code"] == 400:
            return HttpResponseRedirect("/missing")
        elif postVoteRequest.json()["code"] == 403:
            return HttpResponseRedirect("/already")
        elif postVoteRequest.json()["code"] == 404:
            return HttpResponseRedirect("/expired")
        elif postVoteRequest.json()["code"] == 200:
            return HttpResponseRedirect("/success")

        else:
            print(postVoteRequest.json())

    else:
        return redirect("/")
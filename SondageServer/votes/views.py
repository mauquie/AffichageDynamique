from django.shortcuts import render, redirect
import requests

from django.http import JsonResponse

# Create your views here.

def index(request):
    return render(request, "index.html")

def postVote(request):
    '''
        Fonction gérant la connexion des utilisateurs
    '''

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        vote = request.POST.get("vote")

        postVoteRequest = requests.request(method="get", url="http://localhost:8000/api/postVote?vote={}&username={}&password={}".format(vote, username, password))

        return JsonResponse(postVoteRequest.json())

    else:
        return redirect("/")
from django.shortcuts import render, redirect
import requests

from django.http import JsonResponse

# Create your views here.

def index(request):
    if request.user.is_authenticated:
        return render(request, "index.html")
    
    else:
        return redirect("/login/")

def postVote(request):
    '''
        Fonction gérant la connexion des utilisateurs
    '''

    if request.method == "GET":
        username = request.POST.get("username")
        password = request.POST.get("password")
        vote = request.POST.get("vote")

        username = "elowarp"
        password = "mindstorms"
        vote = "1"

        postVoteRequest = requests.request(method="get", url="http://localhost:8000/api/postVote?vote={}&username={}&password={}".format(vote, username, password))

        return JsonResponse(postVoteRequest.json())

    else:
        return JsonResponse({})
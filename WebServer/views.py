from django.shortcuts import render
from django.http import JsonResponse

#Variable de debug car il n'y a pas encore de db
GROUPE = "ADMIN"

# Create your views here.

def index(request):
    return render(request, 'WebServer/index.html')
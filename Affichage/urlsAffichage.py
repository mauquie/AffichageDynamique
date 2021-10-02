from django.urls import path
from . import views as urls


#Urls concernant le serveur Affichage (celui qui est attribué aux écrans)
urlpatterns = [
    path('', urls.index),
]

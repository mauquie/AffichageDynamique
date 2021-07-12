from django.urls import path
from . import views as urls

#Urls concernant le serveur Web (celui utilisé par des êtres humains)
urlpatterns = [
    path("", urls.index),
    path("articles", urls.articles),
    path("articles/ajouter", urls.ajouterArticle),
    path("articles/modifier", urls.modifierArticle),
    path("articles/supprimer", urls.supprimerArticle),
]
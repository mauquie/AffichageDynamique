from django.urls import path
from . import views as urls

#Urls concernant le serveur Web (celui utilisé par des êtres humains)
urlpatterns = [
    path("", urls.index),
    path("login/", urls.loginView),
    path("firstLogin/", urls.firstLogin),
    path("logout/", urls.deconnection),
    path("articles", urls.articles),
    path("articles/ajouter", urls.ajouterArticle),
    path("articles/modifier", urls.modifierArticle),
    path("articles/supprimer", urls.supprimerArticle),
    path("parametres", urls.gestionAffichage),
    path("parametres/sondages", urls.sondages),
    path("parametres/sondages/ajouter", urls.ajouterSondage),
    path("parametres/sondages/modifier", urls.modifierSondage),
    path("parametres/sondages/supprimer", urls.supprimerSondage),
    path("parametres/informations", urls.informations),
    path("parametres/informations/ajouter", urls.ajouterInformation),
    path("parametres/informations/modifier", urls.modifierInformation),
    path("parametres/informations/supprimer", urls.supprimerInformation),
    path("comptes", urls.comptes),
    path("comptes/ajouter", urls.ajouterCompte),
    path("comptes/modifier", urls.modifierCompte),
    path("comptes/toggleActive", urls.toggleActive),
    path("comptes/voir", urls.afficherComptes),
]
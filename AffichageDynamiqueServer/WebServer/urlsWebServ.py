from django.urls import path
from . import views as urls

#Urls concernant le serveur Web (celui utilisé par des êtres humains)
urlpatterns = [
    path("", urls.index),
    path("login/", urls.loginView),
    path("logout/", urls.deconnection),
    path("articles", urls.articles),
    path("articles/ajouter", urls.ajouterArticle),
    path("articles/modifier", urls.modifierArticle),
    path("articles/toggleVisibilite", urls.toggleVisibiliteArticle),
    path("articles/supprimer", urls.supprimerArticle),
    path("parametres", urls.gestionAffichage),
    path("parametres/sondages", urls.sondages),
    path("parametres/sondages/ajouter", urls.ajouterSondage),
    path("parametres/sondages/modifier", urls.modifierSondage),
    path("parametres/sondages/supprimer", urls.supprimerSondage),
    path("parametres/sondages/voirResultats", urls.voirResultatsSondage),
    path("parametres/sondages/toggleVisibilite", urls.toggleVisibiliteSondage),
    path("parametres/informations", urls.informations),
    path("parametres/informations/ajouter", urls.ajouterInformation),
    path("parametres/informations/modifier", urls.modifierInformation),
    path("parametres/informations/supprimer", urls.supprimerInformation),
    path("parametres/informations/toggleVisibilite", urls.toggleVisibiliteInformation),
    path("parametres/ecrans/ajouter", urls.ajouterEcran),
    #path("parametres/ecrans/modifier", urls.modifierEcran),
    #path("parametres/ecrans/supprimer", urls.supprimerEcran),
    path("parametres/pages/ajouter", urls.ajouterPage),
    #path("parametres/pages/modifier", urls.modifierPage),
    #path("parametres/pages/supprimer", urls.supprimerPage),
    path("parametres/modifierPageEcran", urls.modifierAffectation),
    path("comptes", urls.comptes),
    path("comptes/modifier", urls.modifierCompte),
    path("comptes/toggleActive", urls.toggleActive),
    path("comptes/voir", urls.afficherComptes),
    #path("resetPassword", urls.resetPassword),
]
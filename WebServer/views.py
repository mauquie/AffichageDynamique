from django.shortcuts import render
from django.http import JsonResponse

#Variable de debug
GROUPE = "STUDENT"

def index(request, message=""):
    ''' 
        Fonction appelée quand on veut la page initiale où l'on retrouve les actions rapides, et un lien
        vers le reste des actions possibles sur le site.
    '''
    return render(request, 'WebServer/index.html', exInfos("Accueil", {"user_group": GROUPE}, message))

def articles(request, message=""):
    '''
        Fonction appelée quand on veut intéragir d'une quelconque façon avec les articles (ajouter, modifier, supprimer)
        Elle contient une liste des 5 derniers articles postés avec des boutons pour modifier et supprimer un article
        et un autre lien pour créer un article.
    '''
    return render(request, 'WebServer/Articles/index.html', exInfos("Articles", {"user_group": GROUPE}, message))

def ajouterArticle(request, message=""):
    '''
        Fonction appelé quand on veut écrire un article.
    '''
    return render(request, 'WebServer/Articles/ajouter.html', exInfos("Ajouter un article", {"user_group": GROUPE}, message))

def modifierArticle(request, message=""):
    '''
        Fonction appelé quand on veut modifier un article.
    '''
    return render(request, 'WebServer/Articles/modifier.html', exInfos("Modifier un article", {'user_group': GROUPE}, message))

def supprimerArticle(request, message=""):
    '''
        Fonction appelé quand on veut supprimer un article
    '''
    message = "Supprimé avec succès !"
    return articles(request, message)


def exInfos(pageTitle, user, message=""):
    '''
        Fonction appelé quand on veut envoyer des données complémentaires aux Templates comme par exemple le groupe 
        de l'utilisateur ou un message d'information sur une action effectuée

        @Params :
            pageTitle : (string) Nom de la page
            user : (dict) Dictionnaire d'infos sur l'utilisateur
            ?message : (string) Message à transmettre à l'utilisateur sur la page

        @Return :
            dict : Informations complémentaires
    '''
    return {
        "pageTitle": pageTitle,
        "user": user,
        "message": message,
    }
from django.http.response import Http404
from django.shortcuts import render
from django.core.exceptions import PermissionDenied

#Variable de debug
GROUPE = "ADMIN"

def index(request, message=""):
    ''' 
        Fonction appelée quand on veut la page initiale où l'on retrouve les actions rapides, et un lien
        vers le reste des actions possibles sur le site.
    '''
    return render(request, 'WebServer/index.html', exInfos("Accueil", {"user_group": GROUPE}, message))




"""
    Section gérant tout ce qui touche aux articles 

"""
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
    if request.GET.get('id', '') != '':
        return render(request, 'WebServer/Articles/modifier.html', exInfos("Modifier un article", {'user_group': GROUPE}, informations={"title": "Les militaires", "date": "2021-07-10", "articleContent": "ils sont gentils", "image": "/static/IMG/Logo_lycée_Bourdelle.jpg"}))

    else:
        raise Http404()

def supprimerArticle(request, message=""):
    '''
        Fonction appelé quand on veut supprimer un article
    '''
    message = "Supprimé avec succès !"
    return articles(request, message)



"""
    Section gérant tout ce qui touche à la gestion de l'affichage
"""
def gestionAffichage(request):
    if GROUPE != "STUDENT":
        return render(request, 'WebServer/Gestion Affichage/index.html', exInfos("Gestion de l'affichage", {"user_group": GROUPE}))
    
    else: 
        raise PermissionDenied()




"""
    Section gérant tout ce qui touche aux sondages
"""
def sondages(request):
    if GROUPE != "STUDENT":
        return render(request, 'WebServer/Gestion Affichage/Sondages/index.html', exInfos("Sondages", {"user_group": GROUPE}))
    
    else:
        raise PermissionDenied()

def ajouterSondage(request):
    if GROUPE != "STUDENT":
        return render(request, 'WebServer/Gestion Affichage/Sondages/ajouter.html', exInfos("Ajouter un sondage", {"user_group": GROUPE}))
    
    else:
        raise PermissionDenied()

def modifierSondage(request):
    #To-do : Un check du groupe pour savoir si il est au même niveau ou au dessus pour avoir le droit de modifier me sondage
    if GROUPE != "STUDENT":
        return render(request, 'WebServer/Gestion Affichage/Sondages/modifier.html', exInfos("Modifier un sondage", {"user_group": GROUPE}))
    
    else:
        raise PermissionDenied()

def supprimerSondage(request, message=""):
    '''
        Fonction appelé quand on veut supprimer un article
    '''
    message = "Supprimé avec succès !"
    return articles(request, message)




"""
    Section gérant tout ce qui touche aux informations
"""
def informations(request):
    if GROUPE != "STUDENT":
        return render(request, 'WebServer/Gestion Affichage/Informations/index.html', exInfos("Informations", {"user_group": GROUPE}))
    
    else:
        raise PermissionDenied()

def ajouterInformation(request):
    if GROUPE != "STUDENT":
        return render(request, 'WebServer/Gestion Affichage/Informations/ajouter.html', exInfos("Modifier l'information", {"user_group": GROUPE}))
    
    else:
        raise PermissionDenied()

def modifierInformation(request):
    if GROUPE != "STUDENT":
        if(request.GET.get("id", "") != ""):
            return render(request, 'WebServer/Gestion Affichage/Informations/modifier.html', exInfos("Modifier l'information", {"user_group": GROUPE}, informations={"title": "Le nouveaujeu", "informationContent": "je suis le contenu", "date": "2021-08-12", "type": "2"} ))

        else:
            raise Http404()

    else:
        raise PermissionDenied()




"""
    Section contenant les fonctions qui servent pour les views mais que n'en retourne pas
"""
def exInfos(pageTitle, user, message="", informations={}):
    '''
        Fonction appelé quand on veut envoyer des données complémentaires aux Templates comme par exemple le groupe 
        de l'utilisateur ou un message d'information sur une action effectuée

        @Params :
            pageTitle {string}     - Nom de la page
            user {dict}            - Dictionnaire d'infos sur l'utilisateur
            ?message {string}      - Message à transmettre à l'utilisateur sur la page
            ?informations {dict}   - Informations complètes à passer à la page (du genre les données d'un article)

        @Return :
            dict : Informations complémentaires
    '''
    return {
        "pageTitle": pageTitle,
        "user": user,
        "message": message,
        "informations": informations,
    }
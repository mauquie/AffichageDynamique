"""
Gère toutes les vues correspondantes au serveur web de gestion des écrans
"""

from django.http import HttpResponse, HttpResponseForbidden
from django.http.response import Http404
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import get_object_or_404, render, redirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.hashers import make_password
from ApiServer import models 
from . import forms 
from django.contrib.auth.models import Group
from django.contrib import messages
import datetime

from django.template.defaulttags import register

@register.filter
def get_value(dictionary: dict, key: str):
    """
    Template function, trouve la valeur d'une clé dans un
    dictionnaire depuis un template ``Django``

    Args:
        dictionary (dict): Dictionnaire où l'on veut chercher la valeur
        key (str): Clé de la valeur

    Returns:
        Any: Valeur correspondante à la clé
    """
    return dictionary.get(key)

@register.filter(name="get_group")
def get_group(user: models.Users) -> str:
    """
    Template function, récupère le groupe d'un utilisateur et le renvoie

    Args:
        user (models.Users): Utilisateur où l'on veut récupérer le groupe

    Returns:
        string: Le nom du groupe de l'utilisateur
    """
    return list(user.groups.values_list('name', flat=True))[0]

def canEdit(user: models.Users, author: models.Users) -> bool:
    """
    Vérifie qu'un utilisateur peut modifier un objet(Ex: un article) en 
    fonction du niveau (level) de son groupe et du groupe de l'auteur. 

    Si l'auteur à un level plus fort (plus petit) que 
    l'utilisateur alors il ne peut pas modifier l'objet et la fonction 
    retourne False.

    Sinon si l'auteur à un level plus faible ou égal(plus grand ou égal) que l'utilisateur alors
    il peut modifier l'objet et la fonction retourne True

    Args:
        user (models.Users): Utilisateur voulant modifier l'objet
        author (models.Users): Auteur de l'objet

    Returns:
        bool: Autorisation (ou non) de modifier l'objet
    """
    #Récupération des groupes
    userLevel = list(user.groups.values_list('groupsextend', flat=True))[0]
    authorLevel = list(author.groups.values_list('groupsextend', flat=True))[0]

    if authorLevel < userLevel:
        return False

    else:
        return True

@login_required
def index(request: WSGIRequest) -> HttpResponse:
    """
    Renvoie la page d'accueil

    Args:
        request (WSGIRequest): Requête Django

    Returns:
        HttpResponse: Page d'accueil
    """
    return render(request, 'WebServer/index.html', exInfos("Accueil"))


def loginView(request):
    """
    Gère la connexion des utilisateurs

    Si la methode de la requête est ``GET`` alors on renvoit la page de connexion

    Si la methode de la requête est ``POST`` on essaye de l'enregistrer avec les 
    informations que l'utilisateur nous donne, c'est à dire son username et son 
    password

    Args:
        request (WSGIRequest): Requête Django

    Returns:
        HttpResponse: Page de connexion (si pas connecté)
        HttpResponse: Redirection vers la page (si connecté)
    """

    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('/')
        else:
            return render(request, "login.html")

    elif request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        #Si l'utilisateur est bien reconnu
        if user is not None:
            login(request, user)
            
            return redirect('/')

        else:
            #Essaye de trouver un utilisateur avec le même identifiant
            try:
                user = models.Users.objects.get(username=username)
            
            except models.User.DoesNotExist: #S'il ne le trouve pas
                messages.warning(request, "Compte introuvable")

            else: 
                messages.warning(request, "Mot de passe invalide")

            return render(request, "login.html")

"""
    Section gérant tout ce qui touche aux articles 

"""

@permission_required('ApiServer.view_articles')
def articles(request: WSGIRequest) -> HttpResponse:
    """
    Renvoie la page de management des articles, là ou tu peux intéragir avec eux 
    de toutes les facons possibles (ajouter, modifier, supprimer). Elle contient 
    une liste de tous les articles postés depuis toujours sur le site.

    Args:
        request (WSGIRequest): Requête Django

    Returns:
        HttpResponse: Page de management des articles
    """

    articles = models.Articles.objects.all().order_by("-is_shown", "-date_last_modif")
    return render(request, 'WebServer/Articles/index.html', exInfos("Articles", informations=articles))

@permission_required('ApiServer.add_articles')
def ajouterArticle(request: WSGIRequest) -> HttpResponse:
    """
    Gère la création d'article

    Si la methode de la requête est ``GET`` alors on envoit la page de création de 
    l'article

    Si la methode de la requête est ``POST`` alors on vérifie que les données envoyées
    sont conformes au formulaire et si oui on ajoute l'article dans la bdd, si non
    on envoit un message d'erreur

    Args:
        request (WSGIRequest): Requête Django

    Returns:
        HttpResponse: Page d'ajout d'un article
    """
    if request.method == "GET":
        form = forms.ArticleForm()
        return render(request, 'WebServer/Articles/ajouter.html', exInfos("Ajouter un article"))

    elif request.method == "POST":
        form = forms.ArticleForm(request.POST, request.FILES)

        if form.is_valid():
            record = form.save(commit=False)
            record.author = models.Users.objects.filter(pk=request.user.pk)[0]
            record.user_last_modif = models.Users.objects.filter(pk=request.user.pk)[0]
            
            record.save()

            messages.success(request, "Article bien ajouté !")
            return redirect("/articles/ajouter")

        else:
            createErrorMessages(request, form)
            return render(request, "WebServer/Articles/ajouter.html", exInfos("Ajouter un article", form=form))

@permission_required('ApiServer.change_articles')
def modifierArticle(request: WSGIRequest) -> HttpResponse:
    """
    Gère la modification d'un article

    Si la methode de la requête est ``GET``, que le paramètre ``id`` dans l'url est là 
    et qu'il correspond bien à un article alors on envoit la page de modification de 
    l'article sinon on envoie une erreur ``404``

    Si la methode de la requête est ``POST`` alors on vérifie que les données envoyées
    sont conformes au formulaire et si oui on modifie l'article, si non
    on envoit un message d'erreur

    Args:
        request (WSGIRequest): Requête Django

    Returns:
        HttpResponse: Page de modification d'un article
    """
    id = request.GET.get("id", False)

    if id:
        article = get_object_or_404(models.Articles, pk = id)

        # Vérification que l'utilisateur peut modifier l'article
        if not canEdit(request.user, article.author):
            messages.error(request, "Vous n'êtes pas autorisé à modifier cet article.")
            return redirect("/articles")

        if request.method == "GET":
            form = forms.ArticleForm()

            return render(request, 'WebServer/Articles/modifier.html', 
                exInfos("Modifier un article", informations=article, form=form))

        elif request.method == "POST":
            form = forms.ArticleForm(request.POST, request.FILES, instance=article)

            if form.is_valid():
                form.save()

                # On modifie la dernière personne l'ayant modifié
                article.user_last_modif = request.user

                article.save()

                messages.success(request, "Article modifié avec succés !")
                return redirect("/articles/modifier?id="+id)

            else: # Il y a eu un problème
                createErrorMessages(request, form)
                return render(request, "WebServer/Articles/modifier.html", exInfos("Modifier un article", form=form, informations=article))

    else:
        raise Http404


@permission_required('ApiServer.delete_articles')
def supprimerArticle(request: WSGIRequest) -> HttpResponse:
    """
    Gère la suppression d'un article

    Si le paramètre ``id`` est présent et qu'il correspond à un article alors
    on le supprime, sinon on envoit une erreur ``404``

    Args:
        request (WSGIRequest): Requête Django

    Returns:
        HttpResponse: Page de management des articles
    """
    id = request.GET.get("id", False)
    if id:
        article = get_object_or_404(models.Articles, pk = id)

        if canEdit(request.user, article.author):
            article.delete()
            messages.success(request, "Supprimé avec succès !")

        else:
            messages.error(request, "Vous n'êtes pas autorisé à supprimer cet article.")

    else:
        raise Http404
    return redirect("/articles")

@permission_required('ApiServer.change_articles')
def toggleVisibiliteArticle(request: WSGIRequest) -> HttpResponse:
    """
    Gère la visibilité d'un article

    Si le paramètre ``id`` est présent et qu'il correspond à un article alors
    on le modifie la visibilité, sinon on envoit une erreur ``404``.

    Note:
        Lorsque que la visibilité est modifiée, cela veut dire qu'on le met dans 
        l'état inverse où il est, s'il est montré de base alors on le cache et
        inversement. De plus, lors de cette modification, si on l'affiche et que 
        la date de fin est passée, alors on lui rajoute 1 semaine à partir du
        moment où l'on change la visibilité. . 

    Args:
        request (WSGIRequest): Requête Django

    Returns:
        HttpResponse: Page de management des articles
    """
    #Vérification du groupe pour savoir si on peut modifier ou non
    id = request.GET.get("id", False)
    if id:
        article = get_object_or_404(models.Articles, pk = id)

        if canEdit(request.user, article.author):
            if article.is_shown:
                article.is_shown = False

            else:
                if article.date_end < datetime.date.today():
                    article.date_end = changeEndingDate()

                article.is_shown = True

            #On modifie la dernière personne l'ayant modifié
            article.user_last_modif = request.user

            article.save()
            messages.success(request, "Modifié avec succés")

        else:
            messages.error(request, "Vous n'êtes pas autorisé à modifier cet article.")

    else:
        raise Http404

    return redirect("/articles")



"""
    Section gérant tout ce qui touche à la gestion de l'affichage
"""
@permission_required('auth.manage_screens')
def gestionAffichage(request: WSGIRequest) -> HttpResponse:
    """
    Renvoie la page de management des "paramètres" du serveur, c'est à dire
    le fait de pouvoir changer les informations, les sondages et les pages
    associées aux écrans.

    Args:
        request (WSGIRequest): Requête Django

    Returns:
        HttpResponse: Page de management des paramètres du serveur
    """
    return render(request, 'WebServer/Gestion Affichage/index.html', exInfos("Gestion de l'affichage"))



"""
    Section gérant tout ce qui touche aux sondages
"""
@permission_required('ApiServer.view_surveys')
def sondages(request: WSGIRequest) -> HttpResponse:
    """
    Renvoie la page de management des sondages, là ou tu peux intéragir avec eux 
    de toutes les facons possibles (ajouter, modifier, supprimer). Elle contient 
    une liste de tous les sondages postés depuis toujours sur le site.

    Args:
        request (WSGIRequest): Requête Django

    Returns:
        HttpResponse: Page de management des sondages
    """
    surveys = models.Surveys.objects.all().order_by("-is_shown", "date_creation")
    return render(request, 'WebServer/Gestion Affichage/Sondages/index.html', exInfos("Sondages", informations=surveys))

@permission_required('ApiServer.add_surveys')
def ajouterSondage(request: WSGIRequest) -> HttpResponse:
    """
    Gère la création de sondages

    Si la methode de la requête est ``GET`` alors on envoit la page de création de 
    sondages

    Si la methode de la requête est ``POST`` alors on vérifie que les données envoyées
    sont conformes(un sujet, un date de fin, l'état affiché/caché, au moins 2 réponses 
    possibles) et si oui on ajoute le sondage dans la bdd, si non
    on envoit un message d'erreur

    Args:
        request (WSGIRequest): Requête Django

    Returns:
        HttpResponse: Page d'ajout d'un sondage
    """
    if request.method == "GET":
        return render(request, 'WebServer/Gestion Affichage/Sondages/ajouter.html', exInfos("Ajouter un sondage"))
    
    else:
        #Récupération des valeurs données
        answers = request.POST.getlist("answers")
        subject = request.POST.get("subject")
        date_end = request.POST.get("date_end")
        is_shown = request.POST.get("is_shown", False)

        #Vérification des valeurs
        if not subject or not date_end:
            messages.error(request, "Veuillez verifier que toutes les informations sont présentes (Sujet, Date d'expiration)")
            return redirect("/parametres/sondages/ajouter")

        if len(answers) < 2:
            messages.error(request, "Veuillez verifier qu'il y ait au moins 2 réponses proposées")
            return redirect("/parametres/sondages/ajouter")

        #Vérification qu'il n'y ait pas déjà des sondages affichés
        if is_shown:
            potentialShownSurvey = models.Surveys.objects.filter(is_shown=True)
            if len(potentialShownSurvey) > 0:
                potentialShownSurvey[0].is_shown = False
                potentialShownSurvey[0].save()

        #Création du sondage
        survey = models.Surveys()
        survey.subject = subject
        survey.date_end = date_end
        survey.is_shown = is_shown
        survey.author = request.user

        survey.save()

        #Création des réponses associées au sondage
        for answer in answers:
            answersModel = models.Answers()
            answersModel.answer = answer
            answersModel.survey = survey
            answersModel.save()

        messages.success(request, "Sondage ajouté !")
        return redirect("/parametres/sondages")

        
@permission_required('ApiServer.change_surveys')
def modifierSondage(request: WSGIRequest) -> HttpResponse:
    """
    Gère la modification d'un sondage

    Si la methode de la requête est ``GET``, que le paramètre ``id`` dans l'url est là 
    et qu'il correspond bien à un sondage alors on envoit la page de modification du sondage
    sinon on envoie une erreur ``404``

    Si la methode de la requête est ``POST`` alors on vérifie que les données envoyées
    sont conformes(un sujet, un date de fin, l'état affiché/caché, au moins 2 réponses 
    possibles) et si oui on modifie le sondage, si non on envoit un message d'erreur

    Args:
        request (WSGIRequest): Requête Django

    Returns:
        HttpResponse: Page de modification d'un sondage

    """
    if request.method == "GET":
        #Récupération du sondage et des réponses correpondantes
        survey = get_object_or_404(models.Surveys, pk=request.GET.get("id"))
        answers = models.Answers.objects.filter(survey=survey.id)
        
        return render(request, 'WebServer/Gestion Affichage/Sondages/modifier.html', exInfos("Modifier un sondage", informations={"survey": survey, "answers": answers}))

    elif request.method == "POST":
        #Récupération des valeurs données
        id = request.GET.get("id")
        answersList = request.POST.getlist("answers")
        subject = request.POST.get("subject")
        date_end = request.POST.get("date_end")
        is_shown = request.POST.get("is_shown", False)

        #Vérification qu'il n'y ait pas déjà des sondages affichés
        if is_shown:
            potentialShownSurvey = models.Surveys.objects.filter(is_shown=True)
            if len(potentialShownSurvey) > 0:
                potentialShownSurvey[0].is_shown = False
                potentialShownSurvey[0].save()

        #Vérification des valeurs
        if not subject or not date_end:
            messages.error(request, "Veuillez verifier que toutes les informations sont présentes (Question, Date d'expiration)")
            return redirect("/parametres/sondages/ajouter")

        if len(answersList) < 2:
            messages.error(request, "Veuillez verifier qu'il y ait au moins 2 réponses proposées")
            return redirect("/parametres/sondages/ajouter")

        #Modification du sondage déjà existant
        survey = get_object_or_404(models.Surveys, pk=request.GET.get("id"))
        survey.subject = subject
        survey.date_end = date_end
        survey.is_shown = is_shown
        survey.save()

        #Récuperation des réponses correspondante au sondage dans la bdd
        answers = list(models.Answers.objects.filter(survey=survey.id))

        #Suppression des réponses supprimées par l'utilisateur
        for answer in answers:
            if answer.answer not in answersList:
                answer.delete()

        #Ajout des réponses restantes si elles ne sont pas déjà ajoutées
        for answer in answersList:
            #Vérification que la reponse n'est pas déjà associée au sondage
            alreadyInSurvey = False
            for answersSurvey in answers:
                if answersSurvey.answer == answer:
                    alreadyInSurvey = True

            #Si elle ne l'est pas, on l'ajoute
            if not alreadyInSurvey:
                answerModel = models.Reponse()
                answerModel.answer = reponse
                answerModel.survey = survey

                answerModel.save()

        messages.success(request, "Sondage modifié !")
        return redirect("/parametres/sondages/modifier?id="+id)


@permission_required('ApiServer.delete_surveys')
def supprimerSondage(request: WSGIRequest) -> HttpResponse:
    """
    Gère la suppression d'un sondage

    Si le paramètre ``id`` est présent et qu'il correspond à un sondage alors
    on le supprime, sinon on envoit une erreur ``404``

    Args:
        request (WSGIRequest): Requête Django

    Returns:
        HttpResponse: Page de management des sondages

    """
    id = request.GET.get("id", "")
    if id:
        survey = get_object_or_404(models.Surveys, pk=id)
        survey.delete()
        messages.success(request, "Sondage supprimé avec succés !")

    else:
        raise Http404
    return redirect("/parametres/sondages")

@permission_required('ApiServer.change_surveys')
def toggleVisibiliteSondage(request: WSGIRequest) -> HttpResponse:
    """
    Gère la visibilité d'un sondage

    Si le paramètre ``id`` est présent et qu'il correspond à un sondage alors
    on le modifie la visibilité, sinon on envoit une erreur ``404``.

    Note:
        Lorsque que la visibilité est modifiée, cela veut dire qu'on le met dans 
        l'état inverse où il est, s'il est montré de base alors on le cache et
        inversement. De plus, lors de cette modification, si on l'affiche et que 
        la date de fin est passée, alors on lui rajoute 1 semaine à partir du
        moment où l'on change la visibilité. . 

    Args:
        request (WSGIRequest): Requête Django

    Returns:
        HttpResponse: Page de management des sondages

    """
    id = request.GET.get("id", "")
    if id:
        survey = get_object_or_404(models.Surveys, pk=id)
        if survey.is_shown:
            survey.is_shown = False
        
        else:
            if survey.date_end < datetime.date.today():
                survey.date_end = changeEndingDate()

            #Vérification qu'il n'y ait pas déjà des sondages affichés
            potentialShownSurvey = models.Surveys.objects.filter(is_shown=True)
            if len(potentialShownSurvey) > 0:
                potentialShownSurvey[0].is_shown = False
                potentialShownSurvey[0].save()

            survey.is_shown = True

        survey.save()
        
        messages.success(request, "Sondage modifié avec succés")
        return redirect("/parametres/sondages")
    
    else:
        raise Http404

@permission_required('ApiServer.view_surveys')
def voirResultatsSondage(request: WSGIRequest) -> HttpResponse:
    """
    Renvoit la page où les résultats d'un sondage sont affichés

    Si le paramètre ``id`` est passé à l'url et qu'il correspond 
    à un sondage alors on envoit la page, sinon on envoit une erreur
    ``404``

    Args:
        request (WSGIRequest): Requête Django

    Returns:
        HttpResponse: Page de management des articles

    """
    id = request.GET.get("id")

    if id:
        #Récupération des valeurs
        survey = get_object_or_404(models.Surveys, pk=id)
        answers = models.Answers.objects.filter(survey=survey.id)
        votes = models.Votes.objects.filter(survey=survey.id)

        votesDict = {}

        total = 0
        #Ajout des votes sous forme de dictionnaire
        # Id de la reponse : Nb de vote
        for vote in votes:
            if vote.answer.id not in votesDict:
                votesDict[vote.answer.id] = 1
                
            
            else:
                votesDict[vote.answer.id] += 1

            total += 1        


        answersDict = {}

        #Création du dictionnaire contenant les réponses
        # Reponse : id de la reponse
        for answer in answers:
            answersDict[answer.answer] = answer.id

            #Si il n'y a pas de vote pour cette réponse
            #On crée une valeur dans les votes ayant pour id la reponse et
            #comme valeur 0 car il n'y a personne qui a voté pour cette réponse 
            if answer.id not in votesDict:
                votesDict[answer.id] = 0

        #Création du dictionnaire final
        data = {
            "survey": {
                "id": survey.id,
                "date_creation": survey.date_creation,
                "date_end": survey.date_end,
                "subject": survey.subject,
                "is_shown": survey.is_shown,
            },

            "answers": answersDict,

            "votes": votesDict,

            "totalVotes": total

        }
        return render(request, "WebServer/Gestion Affichage/Sondages/voirResultats.html", exInfos("Resultats", informations=data))

    else:
        raise Http404

"""
    Section gérant tout ce qui touche aux informations
"""
@permission_required('ApiServer.view_informations')
def informations(request: WSGIRequest) -> HttpResponse:
    """
    Renvoie la page de management des informations, là ou tu peux intéragir avec elles 
    de toutes les facons possibles (ajouter, modifier, supprimer). Elle contient 
    une liste de toutes les informations postées depuis toujours sur le site.

    Args:
        request (WSGIRequest): Requête Django

    Returns:
        HttpResponse: Page de management des informations
    """
    infos = models.Informations.objects.all()
    return render(request, 'WebServer/Gestion Affichage/Informations/index.html', exInfos("Informations", informations=infos))

@permission_required('ApiServer.add_informations')
def ajouterInformation(request: WSGIRequest) -> HttpResponse:
    """
    Gère la création d'information

    Si la methode de la requête est ``GET`` alors on envoit la page de création d'une
    information

    Si la methode de la requête est ``POST`` alors on vérifie que les données envoyées
    sont conformes au formulaire et si oui on ajoute l'info dans la bdd, si non
    on envoit un message d'erreur

    Args:
        request (WSGIRequest): Requête Django

    Returns:
        HttpResponse: Page d'ajout d'une info
    """
    if request.method == "GET":
        infotypes = models.InfoTypes.objects.all()
        form = forms.InformationForm()
        return render(request, 'WebServer/Gestion Affichage/Informations/ajouter.html', exInfos("Modifier l'information", form=form, informations={"infotypes": infotypes}))
    
    elif request.method == "POST":
        form = forms.InformationForm(request.POST)
        
        if form.is_valid():
            record = form.save(commit=False)
            record.author = request.user
            record.save()

            messages.success(request, "Information crée avec succées !")

        return redirect("/parametres/informations/ajouter")


@permission_required('ApiServer.change_informations')
def modifierInformation(request: WSGIRequest) -> HttpResponse:
    """
    Gère la modification d'une information

    Si la methode de la requête est ``GET``, que le paramètre ``id`` dans l'url est là 
    et qu'il correspond bien à une info alors on envoit la page de modification de 
    l'information sinon on envoie une erreur ``404``

    Si la methode de la requête est ``POST`` alors on vérifie que les données envoyées
    sont conformes au formulaire et si oui on modifie l'info, si non
    on envoit un message d'erreur

    Args:
        request (WSGIRequest): Requête Django

    Returns:
        HttpResponse: Page de modification d'une information
    """
    id = request.GET.get("id", "")
    if(id):
        info = get_object_or_404(models.Informations, pk=id)

        if not canEdit(request.user, info.author):
            messages.error(request, "Vous n'êtes pas autorisé à modifier cette information.")
            return redirect("/parametres/informations")

        if request.method == "GET":
            form = forms.InformationForm()
            infotypes = models.InfoTypes.objects.all()

            return render(request, 'WebServer/Gestion Affichage/Informations/modifier.html', exInfos("Modifier l'information", form = form, informations={"info": info, "infotypes": infotypes}))
        
        elif request.method == "POST":
            form = forms.InformationForm(request.POST, instance=info)

            if form.is_valid():
                form.save()

                messages.success(request, "Information bien mise à jour !")
                return redirect("/parametres/informations")

            else:
                createErrorMessages(request, form)
                infotypes = models.InfoTypes.objects.all()
                return render(request, 'WebServer/Gestion Affichage/Informations/modifier.html', exInfos("Modifier l'information", form = form, informations={"info": info, "infotypes": infotypes}))


    else:
        raise Http404


@permission_required('ApiServer.delete_informations')
def supprimerInformation(request: WSGIRequest) -> HttpResponse:
    """
    Gère la suppression d'une information

    Si le paramètre ``id`` est présent et qu'il correspond à une info alors
    on la supprime, sinon on envoit une erreur ``404``

    Args:
        request (WSGIRequest): Requête Django

    Returns:
        HttpResponse: Page de management des informations
    """
    id = request.GET.get('id', '')
    if id:  
        info = get_object_or_404(models.Informations, pk=id)

        if canEdit(request.user, info.author):
            info.delete()
            messages.success(request, "Supprimé avec succés")
            
        else:
            messages.error(request, "Vous n'êtes pas autorisé à supprimer cette information.")
            
    else:
        raise Http404

    return redirect("/parametres/informations")

@permission_required('ApiServer.change_informations')
def toggleVisibiliteInformation(request: WSGIRequest) -> HttpResponse:
    """
    Gère la visibilité d'une information

    Si le paramètre ``id`` est présent et qu'il correspond à une info alors
    on le modifie la visibilité, sinon on envoit une erreur ``404``.

    Note:
        Lorsque que la visibilité est modifiée, cela veut dire qu'on le met dans 
        l'état inverse où il est, s'il est montré de base alors on le cache et
        inversement. De plus, lors de cette modification, si on l'affiche et que 
        la date de fin est passée, alors on lui rajoute 1 semaine à partir du
        moment où l'on change la visibilité. 

    Args:
        request (WSGIRequest): Requête Django

    Returns:
        HttpResponse: Page de management des informations
    """
    id = request.GET.get('id', "")
    if(id):
        info = get_object_or_404(models.Informations, pk=id)

        if not canEdit(request.user, info.author):
            messages.error(request, "Vous n'êtes pas autorisé à modifier cette information.")
            return redirect("/parametres/informations")

        if info.is_shown:
            info.is_shown = False
            messages.success(request, "Information cachée !")

        else:
            if info.date_end < datetime.date.today():
                info.date_end = changeEndingDate()

            info.is_shown = True
            messages.success(request, "Information affichée !")

        info.save()

    return redirect("/parametres/informations")




"""
    Section gérant tout ce qui touche aux comptes
"""
@login_required
def comptes(request: WSGIRequest) -> HttpResponse:
    """
    Renvoit la page de gestion des comptes

    Args:
        request (WSGIRequest): Requête Django

    Returns:
        HttpResponse: Page de gestion des comptes
    """
    #Récuperation des articles crée par l'user
    articles = models.Articles.objects.all().filter(author_id = request.user.id)
    surveys = models.Surveys.objects.all().filter(author_id = request.user.id)
    return render(request, 'WebServer/Comptes/index.html', exInfos("Gestion du compte", informations={"articles": articles, "surveys": surveys}))

@login_required
def modifierCompte(request: WSGIRequest) -> HttpResponse:
    """
    Gère la modification de compte

    Si la methode de la requête est ``GET``, et qu'il n'y a pas ``id`` alors
    on envoit la page de modification de son propre compte, mais s'il y a l'id
    et qu'il correspond à un compte alors on renvoit la page pour modifier le 
    compte en question (s'il n'a pas les droits il ne pourra pas le modifier mais
    seulement voir une partie des informations)

    Si la methode de la requête est ``POST``, et que les informations transmises
    correspondes au formulaire adequat alors on modifie le compte, sinon on envoie
    une erreur.

    Args:
        request (WSGIRequest): Requête Django

    Returns:
        HttpResponse: Page de modification de compte (son propre compte ou celui d'un
            autre)
    """
    #Si l'user veut modifier un compte particulier
    id = request.GET.get('id', False)
    if request.method == "GET":
        #Verification qu'il a les droits pour visionner le compte
        if id:
            #Si l'utilisateur est trouvé on l'affiche sinon on renvoie un 404
            user = get_object_or_404(models.Users, pk=id)

            if user.id == request.user.id:
                return redirect("/comptes/modifier")

            articles = models.Articles.objects.filter(author=user)
            surveys = models.Surveys.objects.filter(author=user)
            groups = models.GroupsExtend.objects.all()

            if request.user.has_perm('auth.manage_accounts'):
                canEdit = True
            else:
                canEdit = False

            return render(request, 'WebServer/Comptes/modifierCompteAutre.html', exInfos("Modifier un compte", informations={"user": user, "articles": articles, "surveys": surveys, "canEdit": canEdit, "groups": groups}))
            

        else:   
            return render(request, "WebServer/Comptes/modifierComptePerso.html", exInfos("Modifier mon compte"))

    else:
        if id:
            #Si l'user veut modifier un compte particulier
            if request.user.has_perm("ApiServer.change_users"):
                user = get_object_or_404(models.Users, pk=id)
                form = forms.changeOthersAccount(request.POST, request.FILES, instance=user)

                if form.is_valid():
                    form.save()

                    messages.success(request, "Compte modifié !")
                    return redirect("/comptes/modifier?id="+id)
                
                else:
                    createErrorMessages(request, form)
                    return render(request, "WebServer/Comptes/modifierCompteAutre.html", exInfos("Modifier un compte", form = form, informations=user))
            
            else:
                return PermissionDenied()

        else:
            #Modification de son propre compte
            form = forms.changeOwnAccount(request.POST, request.FILES, instance=request.user)

            if form.is_valid():
                password = request.POST.get("password", False)
                passwordConfirm = request.POST.get("password_confirm", False)

                #Verification de si l'user veut modifier son mot de passe
                if password :
                    if passwordConfirm == password:
                        #Changement du mot de passe
                        request.user.password = make_password(password)
                        request.user.save()

                    else:
                        messages.error(request, "Les mots de passes ne sont pas identiques")

                        return render(request, "WebServer/Comptes/modifierComptePerso.html")
                    
                #Sauvegarde du reste des informations
                form.save()

                #Mise à jour du cookie de session
                update_session_auth_hash(request, request.user)

                messages.success(request, "Compte modifié !")

                return render(request, "WebServer/Comptes/modifierComptePerso.html", exInfos("Modifier mon compte"))
            else:
                createErrorMessages(request, form)
                return render(request, "WebServer/Comptes/modifierComptePerso.html", exInfos("Modifier mon compte", form=form))

@login_required
def toggleActive(request: WSGIRequest) -> HttpResponse:
    """
    Gère l'activité d'un compte

    Si un compte est actif alors il peut utiliser le site mais s'il n'est pas
    actif alors il lui est impossible d'acceder au site comme si il n'avait plus 
    de compte OR on garde quand même toutes ses informations et on peut réactiver 
    le compte à tout moment

    Args:
        request (WSGIRequest): Requête Django

    Returns:
        HttpResponse: Page de gestion des comptes
    """
    id = request.GET.get("id", False)
    #Si l'user desactive un autre compte
    if id:
        if request.user.has_perm("ApiServer.delete_users"):
            user = get_object_or_404(models.Users, pk = id)

            if user.is_active:
                user.is_active = False
                messages.success(request, "Compte désactivé !")

            else:
                user.is_active = True
                messages.success(request, "Compte réactivé !")

            user.save()

        else:
            return PermissionDenied()

    else: #Sinon il desactive son compte
        if request.user.is_active:
            request.user.is_active = False
            messages.success(request, "Compte désactivé ! Pour le reactiver, veuillez vous adresser à un administrateur")

        request.user.save()

    return redirect("/comptes/voir")

def deconnection(request: WSGIRequest) -> HttpResponse:
    """
    Gère la deconnection

    Args:
        request (WSGIRequest): Requête Django

    Returns:
        HttpResponse: Page de connexion
    """
    logout(request)
    return redirect("/")

@permission_required('ApiServer.view_users')
def afficherComptes(request: WSGIRequest) -> HttpResponse:
    """
    Gère les comptes de tous les utilisateurs

    Affiche une liste avec tous les utilisateurs enregistrés sur le site
    avec toutes les actions possibles (modifier le compte, le supprimer, le
    désactiver)

    Args:
        request (WSGIRequest): Requête Django

    Returns:
        HttpResponse: Page de gestion de tous les utilisateurs
    """
    #Récupération des comptes
    users = models.Users.objects.all()

    #Tri en fonction du nom de famille
    users = users.order_by("last_name", "username")

    return render(request, 'WebServer/Comptes/voirToutComptes.html', exInfos("Utilisateurs", informations={"users": users}))


"""
    Section gérant tout ce qui touche aux écrans
"""
@permission_required("ApiServer.add_screens")
def ajouterEcran(request: WSGIRequest) -> HttpResponse:
    """
    Gère l'ajout de nouveaux écrans

    Si la methode de la requête est ``GET`` alors on envoie la page d'ajout
    sinon on compare les informations données au formulaire et si elles sont
    conformes on ajoute l'écran à la BDD

    Args:
        request (WSGIRequest): Requête Django

    Returns:
        HttpResponse: Page d'ajout des écrans
    """
    if request.method == "GET":
        return render(request, "WebServer/Gestion Affichage/Ecrans/ajouterEcran.html")

    elif request.method == "POST":
        form = forms.ScreenForm(request.POST)
        
        if form.is_valid():
            form.save()
            messages.success(request, "Ajouté avec succés")
        
        else:
            createErrorMessages(request, form)
        
    return render(request, "WebServer/Gestion Affichage/Ecrans/ajouterEcran.html")
    
@permission_required("ApiServer.change_screens")
def modifierEcran(request: WSGIRequest) -> HttpResponse:
    """
    Gère la modification des écrans

    Si la methode de la requête est ``GET`` et qu'il y a le paramètre ``id``
    alors on envoie la page de modification sinon on compare les informations 
    données au formulaire et si elles sont conformes on modifie l'écran 

    Args:
        request (WSGIRequest): Requête Django

    Returns:
        HttpResponse: Page de modification des écrans

    Todo:
        La page qui liste tous les écrans et un lien vers la page de modif des écrans
    """
    id = request.GET.get("id", "")
    if id:
        if request.method == "GET":
            ecran = get_object_or_404(models.Display, pk=id)
            return render(request, 'WebServer/Gestion Affichage/Ecrans/modifierEcran.html', exInfos("Modifier un écran", informations=ecran))

        elif request.method == "POST":
            ecran = get_object_or_404(models.Display, pk=id)
            form = forms.ScreenForm(request.POST, instance=ecran)

            if form.is_valid():
                form.save()
                messages.success(request, "Modifié avec succés")
            else:
                createErrorMessages(request, form)
            
            return render(request, 'WebServer/Gestion Affichage/Ecrans/modifierEcran.html', exInfos("Modifier un écran", form=form, informations=ecran))

    else:
        raise Http404

@permission_required("ApiServer.delete_screens")
def supprimerEcran(request: WSGIRequest) -> HttpResponse:
    """
    Gère la suppresion d'un écran

    Args:
        request (WSGIRequest): Requête Django

    Returns:
        HttpResponse: Page de suppression des écrans

    Todo:
        Code à faire et fonction à implémenter dans des pages
    """
    return redirect("/parametres")

@permission_required("ApiServer.add_pages")
def ajouterPage(request: WSGIRequest) -> HttpResponse:
    """
    Gère l'ajout de nouvelles pages

    Si la methode de la requête est ``GET`` alors on envoie la page d'ajout
    sinon on compare les informations données au formulaire et si elles sont
    conformes on ajoute la page à la BDD

    Args:
        request (WSGIRequest): Requête Django

    Returns:
        HttpResponse: Page d'ajout des pages
    """
    if request.method == "GET":
        return render(request, "WebServer/Gestion Affichage/Ecrans/ajouterPage.html")

    elif request.method == "POST":
        form = forms.PageForm(request.POST)
        
        if form.is_valid():
            form.save()
            messages.success(request, "Ajouté avec succés")
        
        else:
            createErrorMessages(request, form)
        
    return render(request, "WebServer/Gestion Affichage/Ecrans/ajouterPage.html")
    
@permission_required("ApiServer.change_pages")
def modifierPage(request: WSGIRequest) -> HttpResponse:
    """
    Gère la modification des pages

    Si la methode de la requête est ``GET`` et qu'il y a le paramètre ``id``
    alors on envoie la page de modification sinon on compare les informations 
    données au formulaire et si elles sont conformes on modifie la page 

    Args:
        request (WSGIRequest): Requête Django

    Returns:
        HttpResponse: Page de modification des pages

    Todo:
        La page qui liste toutes les pages et un lien vers la page de modif des pages
    """
    id = request.GET.get("id", "")
    if id:
        if request.method == "GET":
            ecran = get_object_or_404(models.Page, pk=id)
            return render(request, 'WebServer/Gestion Affichage/Ecrans/modifierPage.html', exInfos("Modifier une page", informations=ecran))

        elif request.method == "POST":
            ecran = get_object_or_404(models.Page, pk=id)
            form = forms.PageForm(request.POST, instance=ecran)

            if form.is_valid():
                form.save()
                messages.success(request, "Modifié avec succés")
            else:
                createErrorMessages(request, form)
            
            return render(request, 'WebServer/Gestion Affichage/Ecrans/modifierPage.html', exInfos("Modifier une page", form=form, informations=ecran))

    else:
        raise Http404

@permission_required("ApiServer.delete_pages")
def supprimerPage(request: WSGIRequest) -> HttpResponse:
    """
    Gère la suppresion d'une page

    Args:
        request (WSGIRequest): Requête Django

    Returns:
        HttpResponse: Page de suppression des pages

    Todo:
        Code à faire et fonction à implémenter dans des pages
    """
    return redirect("/parametres")

@permission_required("auth.manage_affectation_pages_screens")
def modifierAffectation(request: WSGIRequest) -> HttpResponse:
    """
    Gère l'affection de page aux écrans

    Si la methode de la requête est ``GET`` alors on envoit la page de modification
    de l'affection page <-> écran

    Si la methode de la requête est ``POST``, qu'il y a bien une page donnée et au moins
    un écran selectionné alors on modifie l'affection dans la base de données

    Args:
        request (WSGIRequest): Requête Django

    Returns:
        HttpResponse: Page de modification de l'affection page <-> écran
    """
    if request.method == "GET":
        screens = models.Screens.objects.all().order_by("name")
        pages = models.Pages.objects.all()
        return render(request, 'WebServer/Gestion Affichage/Ecrans/modifierLaffectation.html', exInfos("Modification des écrans", informations={"screens": screens, "pages": pages}))
    
    elif request.method == "POST":
        #Si l'user fourni une page précise, on le recupère sinon on met la page par defaut (correspondant au -1 pour l'identifiant)
        pageId = int(request.POST.get("page", -1))
        
        #Si l'id fourni est différent de -1 donc que l'user l'a fourni
        if pageId > -1:
            #Recherche de la page correspondante
            page = models.Pages.objects.filter(pk = pageId)[0]

        #Si l'user a donné une liste d'écrans à modifier
        if request.POST.getlist("screens", ""):

            #Pour tous les écrans dans cette liste
            for i in range(len(request.POST.getlist("screens"))):
                #Id de l'écran qu'on modifie dans cette itération
                screenId = request.POST.getlist("screens")[i]

                #L'écran correspondant à l'id
                screens = models.Screens.objects.filter(pk = screenId)

                #Si l'écran n'est pas trouvé
                if len(screens) < 1:
                    messages.error(request, "Il y a eu un problème, l'écran avec l'identifiant " + screenId + " n'a pas pu être mis à jour")

                #S'il est trouvé
                else:
                    screen = screens[0]
                    
                    #Si on a pas trouvé la page ou que l'user ne souhaite pas de page en particulier
                    if pageId == -1:
                        screen.page = None

                    #Si l'user veut une page en particulier qu'on a trouvé
                    else:
                        screen.page = page

                    #Sauvegarde
                    screen.save()

            messages.success(request, "Les écrans ont bien été mis à jour !")

        
        return redirect("/parametres/modifierPageEcran")


"""
    Section contenant les fonctions qui servent pour les views mais que n'en retourne pas
"""
def exInfos(pageTitle, informations={}, form={}):
    """
    Fonction appelée quand on veut envoyer des données complémentaires aux Templates comme par exemple le groupe 
    de l'utilisateur ou un message d'information sur une action effectuée
    
    Args:
        pageTitle (string): Nom de la page
        informations (dict, optionnel): Informations complètes à passer à la page (Ex: les données d'un article)
        form (ModelForm, optionnel): Formulaire à donner au Template
       
    Returns:
        dict: Informations complémentaires
    """
    return {
        "pageTitle": pageTitle,
        "informations": informations,
        "form": form,
    }

def createErrorMessages(request, form):
    """
    Créer depuis un formulaire, une liste de message d'erreur prête à être passée aux Templates pour les
    afficher à l'utilisateur.

    Args:
        form (ModelForm): Formulaire non valide

    """
    errors = form.errors.as_data().values()
    for value in errors:
        messages.error(request, value[0].message)

def changeEndingDate():
    """
    Renvoie la date correspondant au jour une semaine après l'exécution de cette fonction
    
    Returns:
        datetime - Date aujourd'hui + 7 jours
    """
    date = datetime.date.today() + datetime.timedelta(days=7)
    return date
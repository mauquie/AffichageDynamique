from django.http.response import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.hashers import make_password
from ApiServer import models 
from . import forms 
from django.contrib.auth.models import Group
from django.contrib import messages


@login_required
def index(request):
    ''' 
        Fonction appelée quand on veut la page initiale où l'on retrouve les actions rapides, et un lien
        vers le reste des actions possibles sur le site.
    '''
    return render(request, 'WebServer/index.html', exInfos("Accueil"))


def loginView(request):
    '''
        Fonction gérant la connexion des utilisateurs
    '''
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
            #Si un mot de passe n'est pas rentré, il peut s'agir de la première connexion d'un utilisateur
            if password == "":
                #Essaye de trouver un utilisateur avec le même identifiant
                try:
                    user = models.User.objects.get(username=username)
                
                except models.User.DoesNotExist: #S'il ne le trouve pas
                    messages.warning(request, "Compte introuvable")
                    return render(request, "login.html")

                else: 
                    #S'il un utilisateur est trouvé et qu'il ne s'est pas encore connecté une seule fois
                    if user.last_login == None:
                        return redirect('/firstLogin/?username=' + username)
                    
                    else: 
                        messages.warning(request, "Identifiants invalides")
                        return render(request, "login.html")

            messages.warning(request, "Identifiants invalides")
            return render(request, "login.html")

def firstLogin(request):
    '''
        Fonction gérant la première connexion au site internet pour chaque utilisateur
    '''
    if request.method == "GET":
        #Si l'utilisateur est déjà connecté, il n'a pas à accéder à cette page
        if request.user.is_authenticated:
            return redirect('/')

        else:
            #Essaye de voir s'il y a les paramètres demandés pour l'authentification
            try:
                username = request.GET['username']

            except KeyError: #Si le pseudo n'est pas rentré
                return redirect("/login/")

            else: 
                #Vérification de la présence des paramètres
                try:
                    password = request.GET['password']   
                    passwordConfirm = request.GET['passwordConfirm'] 

                except KeyError: #S'il manque des paramètres
                    return render(request, "premiereConnexion.html")

                else:
                    #Si les mots de passe sont identiques
                    if password == passwordConfirm:
                    
                        #Essaye de voir si l'utilisateur existe dans la base de donnée
                        try:
                            user = models.User.objects.get(username=username)

                        except models.User.DoesNotExist:
                            return redirect('/login/')

                        else:
                            #Si c'est la première fois qu'il se connecte
                            if user.last_login == None:
                                #Définition le mot de passe du compte
                                user.set_password(password)
                                user.save()

                                #Vérification si le mot de passe et le pseudo sont justes et que tout s'est bien passé
                                user = authenticate(request, username=username, password=password)
                                if user is not None:
                                    #Connexion au compte et redirection vers l'accueil
                                    login(request, user)
                                    return redirect("/")

                                else: 
                                    messages.error(request, "Erreur inconnue")
                                    return render(request, "premiereConnexion.html")

                            else:
                                return redirect('/login/')

                    else:
                        messages.warning(request, "Mots de passes non identiques")
                        return render(request, "premiereConnexion.html")  


"""
    Section gérant tout ce qui touche aux articles 

"""

@permission_required('ApiServer.view_article')
def articles(request):
    '''
        Fonction appelée quand on veut intéragir d'une quelconque façon avec les articles (ajouter, modifier, supprimer)
        Elle contient une liste des 5 derniers articles postés avec des boutons pour modifier et supprimer un article
        et un autre lien pour créer un article.
    '''
    return render(request, 'WebServer/Articles/index.html', exInfos("Articles"))

@permission_required('ApiServer.add_article')
def ajouterArticle(request):
    '''
        Fonction appelé quand on veut écrire un article.
    '''
    return render(request, 'WebServer/Articles/ajouter.html', exInfos("Ajouter un article"))

@permission_required('ApiServer.change_article')
def modifierArticle(request):
    '''
        Fonction appelé quand on veut modifier un article.
    '''
    #To-do : Verification du groupe / utilisateur pour voir sil a le droit de modifier l'article
    if request.GET.get('id', '') != '':
        return render(request, 'WebServer/Articles/modifier.html', exInfos("Modifier un article", informations={"title": "Les militaires", "date": "2021-07-10", "articleContent": "ils sont gentils", "image": "/static/IMG/Logo_lycée_Bourdelle.jpg"}))

    else:
        raise Http404()

@permission_required('ApiServer.delete_article')
def supprimerArticle(request):
    '''
        Fonction appelé quand on veut supprimer un article
    '''
    messages.success(request, "Supprimé avec succès !")
    return redirect("/articles")

@permission_required('ApiServer.change_article')
def toggleVisibiliteArticle(request):
    #Vérification du groupe pour savoir si on peut modifier ou non
    messages.success("Modifié avec succés")
    return redirect("/articles")


"""
    Section gérant tout ce qui touche à la gestion de l'affichage
"""
@permission_required('ApiServer.manage_screen')
def gestionAffichage(request):
    return render(request, 'WebServer/Gestion Affichage/index.html', exInfos("Gestion de l'affichage"))





"""
    Section gérant tout ce qui touche aux sondages
"""

@permission_required('ApiServer.view_sondage')
def sondages(request):
    return render(request, 'WebServer/Gestion Affichage/Sondages/index.html', exInfos("Sondages"))

@permission_required('ApiServer.add_sondage')
def ajouterSondage(request):
    return render(request, 'WebServer/Gestion Affichage/Sondages/ajouter.html', exInfos("Ajouter un sondage"))

@permission_required('ApiServer.change_sondage')
def modifierSondage(request):
    #To-do : Un check du groupe pour savoir si il est au même niveau ou au dessus pour avoir le droit de modifier me sondage
    return render(request, 'WebServer/Gestion Affichage/Sondages/modifier.html', exInfos("Modifier un sondage"))


@permission_required('ApiServer.delete_sondage')
def supprimerSondage(request):
    '''
        Fonction appelé quand on veut supprimer un article
    '''
    messages.success(request, "Sondage supprimé avec succés !")
    return redirect("/parametres/sondages")




"""
    Section gérant tout ce qui touche aux informations
"""
@permission_required('ApiServer.view_information')
def informations(request):
    return render(request, 'WebServer/Gestion Affichage/Informations/index.html', exInfos("Informations", {"user_group": GROUPE}, messages))

@permission_required('ApiServer.add_information')
def ajouterInformation(request):
    return render(request, 'WebServer/Gestion Affichage/Informations/ajouter.html', exInfos("Modifier l'information"))
    

@permission_required('ApiServer.change_information')
def modifierInformation(request):
    if(request.GET.get("id", "") != ""):
        return render(request, 'WebServer/Gestion Affichage/Informations/modifier.html', exInfos("Modifier l'information", informations={"title": "Le nouveaujeu", "informationContent": "je suis le contenu", "date": "2021-08-12", "type": "2"} ))

    else:
        raise Http404()


@permission_required('ApiServer.delete_information')
def supprimerInformation(request):
    messages.success(request, "Supprimé avec succés")
    return redirect("/parametres/informations")




"""
    Section gérant tout ce qui touche aux comptes
"""
def comptes(request):
    return render(request, 'WebServer/Comptes/index.html', exInfos("Gestion du compte"))

@permission_required('ApiServer.add_user')
def ajouterCompte(request):
    if request.method == "GET":
        form = forms.UserForm()
        return render(request, 'WebServer/Comptes/ajouter.html', exInfos("Ajouter un compte", form=form))

    elif request.method == "POST":
        form = forms.UserForm(request.POST)

        #Vérification du formulaire
        if form.is_valid():
            #Sauvegarde dans la DB
            form.save()
            
            #Ajout de l'utilisateur dans le groupe choisi
            user = models.User.objects.get(username=request.POST.get("username"))
            group = Group.objects.get(id=request.POST.get("groups"))
            user.groups.add(group)

            #Retour du status
            informations = exInfos(
                pageTitle = "Ajouter un compte",
                form = form,
            )

            messages.success(request, "Utilisateur crée avec succés")
            return render(request, 'WebServer/Comptes/ajouter.html', informations)
            

        else:
            #Recuperation des erreurs
            createErrorMessages(request, form)

            #Renvoie du formulaire et des erreurs
            informations = exInfos(
                pageTitle = "Ajouter un compte",
                form = form,
            )

            return render(request, 'WebServer/Comptes/ajouter.html', informations)

@login_required
def modifierCompte(request):
    #Si l'user veut modifier un compte particulier
    id = request.GET.get('id', False)
    if request.method == "GET":
        #Verification qu'il a les droits pour visionner le compte
        if id:
            if request.user.has_perm("ApiServer.change_user"):
                #Si l'utilisateur est trouvé on l'affiche sinon on renvoie un 404
                user = get_object_or_404(models.User, pk=id)
                return render(request, 'WebServer/Comptes/modifierCompteAutre.html', exInfos("Modifier un compte", informations=user))
            
            else: 
                return redirect("/comptes/voir")

        else:   
            return render(request, "WebServer/Comptes/modifierComptePerso.html", exInfos("Modifier mon compte"))

    else:
        if id:
            #Si l'user veut modifier un compte particulier
            if request.user.has_perm("ApiServer.change_user"):
                user = get_object_or_404(models.User, pk=id)
                form = forms.changeOthersAccount(request.POST, request.FILES, instance=user)

                if form.is_valid():
                    form.save()

                    messages.success(request, "Compte modifié !")
                    return render(request, "WebServer/Comptes/modifierCompteAutre.html", exInfos("Modifier un compte", form=form, informations=user))
                
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
def toggleActive(request):
    id = request.GET.get("id", False)
    #Si l'user desactive son propre compte ou un autre compte
    if id:
        if request.user.has_perm("ApiServer.delete_user"):
            user = get_object_or_404(models.User, pk = id)

            if user.is_active:
                user.is_active = False
                messages.success(request, "Compte désactivé !")

            else:
                user.is_active = True
                messages.success(request, "Compte réactivé !")

            user.save()

        else:
            return PermissionDenied()
    else:
        if request.user.is_active:
            request.user.is_active = False
            messages.success(request, "Compte désactivé ! Pour le reactiver, veuillez vous adresser à un administrateur")

        request.user.save()

    return redirect("/comptes/voir")

def deconnection(request):
    logout(request)
    return redirect("/")

@permission_required('ApiServer.view_user')
def afficherComptes(request):
    #Récupération des comptes
    users = models.User.objects.all()

    #Tri en fonction du nom de famille
    users = users.order_by("last_name", "username")

    return render(request, 'WebServer/Comptes/voirToutComptes.html', exInfos("Utilisateurs", informations={"users": users}))





"""
    Section contenant les fonctions qui servent pour les views mais que n'en retourne pas
"""
def exInfos(pageTitle, user={}, informations={}, form={}):
    '''
        Fonction appelé quand on veut envoyer des données complémentaires aux Templates comme par exemple le groupe 
        de l'utilisateur ou un message d'information sur une action effectuée

        @Params :
            pageTitle {string}     - Nom de la page
            ?userGr {dict}         - Dictionnaire d'infos sur l'utilisateur
            ?message {dict}        - Message à transmettre à l'utilisateur sur la page (text: "", type: "success" | "danger" | "warning" )
            ?informations {dict}   - Informations complètes à passer à la page (Ex: les données d'un article)
            ?form {ModelForm}      - Formulaire à donner au Template
           
        @Return :
            dict : Informations complémentaires
    '''
    return {
        "pageTitle": pageTitle,
        "informations": informations,
        "form": form,
    }

def createErrorMessages(request, form):
    '''
        Fonction créeant depuis un formulaire, une liste de message d'erreur prête à être passée aux Templates pour les
        afficher à l'utilisateur.

        @Params :
            form {ModelForm}     - Formulaire non valide

    '''
    errors = form.errors.as_data().values()
    for value in errors:
        messages.error(request, value[0].message)

from django.http.response import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.hashers import make_password
from ApiServer import models 
from . import forms 
from django.contrib.auth.models import Group

#Variable de debug
GROUPE = "ADMIN"

@login_required
def index(request, messages=[]):
    ''' 
        Fonction appelée quand on veut la page initiale où l'on retrouve les actions rapides, et un lien
        vers le reste des actions possibles sur le site.
    '''
    return render(request, 'WebServer/index.html', exInfos("Accueil", {"user_group": GROUPE}, messages))


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
                    return render(request, "login.html", {"messages": [{"type": "warning", "text": "Compte introuvable"}]})

                else: 
                    #S'il un utilisateur est trouvé et qu'il ne s'est pas encore connecté une seule fois
                    if user.last_login == None:
                        return redirect('/firstLogin/?username=' + username)
                    
                    else: 
                        return render(request, "login.html", {"messages": [{"type": "warning", "text": "Identifiants invalides"}]})

            return render(request, "login.html", {"messages": [{"type": "warning", "text": "Identifiants invalides"}]})

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
                                    return render(request, "premiereConnexion.html", {"messages": [{"type": "danger", "text": "Erreur inconnue"}]})

                            else:
                                return redirect('/login/')

                    else:
                        return render(request, "premiereConnexion.html", {"messages": [{"type": "warning", "text": "Mots de passes non identiques"}]})  


"""
    Section gérant tout ce qui touche aux articles 

"""

@permission_required('ApiServer.view_article')
def articles(request, messages=[]):
    '''
        Fonction appelée quand on veut intéragir d'une quelconque façon avec les articles (ajouter, modifier, supprimer)
        Elle contient une liste des 5 derniers articles postés avec des boutons pour modifier et supprimer un article
        et un autre lien pour créer un article.
    '''
    return render(request, 'WebServer/Articles/index.html', exInfos("Articles", {"user_group": GROUPE}, messages))

@permission_required('ApiServer.add_article')
def ajouterArticle(request, messages=[]):
    '''
        Fonction appelé quand on veut écrire un article.
    '''
    return render(request, 'WebServer/Articles/ajouter.html', exInfos("Ajouter un article", {"user_group": GROUPE}, messages))

@permission_required('ApiServer.change_article')
def modifierArticle(request, messages=[]):
    '''
        Fonction appelé quand on veut modifier un article.
    '''
    #To-do : Verification du groupe / utilisateur pour voir sil a le droit de modifier l'article
    if request.GET.get('id', '') != '':
        return render(request, 'WebServer/Articles/modifier.html', exInfos("Modifier un article", {'user_group': GROUPE}, informations={"title": "Les militaires", "date": "2021-07-10", "articleContent": "ils sont gentils", "image": "/static/IMG/Logo_lycée_Bourdelle.jpg"}))

    else:
        raise Http404()

@permission_required('ApiServer.delete_article')
def supprimerArticle(request, messages=[]):
    '''
        Fonction appelé quand on veut supprimer un article
    '''
    message = {"text": "Supprimé avec succès !", "type":"success"}
    return articles(request, message)

@permission_required('ApiServer.change_article')
def toggleVisibiliteArticle(request):
    #Vérification du groupe pour savoir si on peut modifier ou non
    message = [{"type": "success", "text": "Modifié avec succée"}]
    return articles(request, message)


"""
    Section gérant tout ce qui touche à la gestion de l'affichage
"""
@permission_required('ApiServer.manage_screen')
def gestionAffichage(request):
    if GROUPE != "STUDENT":
        return render(request, 'WebServer/Gestion Affichage/index.html', exInfos("Gestion de l'affichage", {"user_group": GROUPE}))
    
    else: 
        raise PermissionDenied()




"""
    Section gérant tout ce qui touche aux sondages
"""

@permission_required('ApiServer.view_sondage')
def sondages(request):
    if GROUPE != "STUDENT":
        return render(request, 'WebServer/Gestion Affichage/Sondages/index.html', exInfos("Sondages", {"user_group": GROUPE}))
    
    else:
        raise PermissionDenied()

@permission_required('ApiServer.add_sondage')
def ajouterSondage(request):
    if GROUPE != "STUDENT":
        return render(request, 'WebServer/Gestion Affichage/Sondages/ajouter.html', exInfos("Ajouter un sondage", {"user_group": GROUPE}))
    
    else:
        raise PermissionDenied()

@permission_required('ApiServer.change_sondage')
def modifierSondage(request):
    #To-do : Un check du groupe pour savoir si il est au même niveau ou au dessus pour avoir le droit de modifier me sondage
    if GROUPE != "STUDENT":
        return render(request, 'WebServer/Gestion Affichage/Sondages/modifier.html', exInfos("Modifier un sondage", {"user_group": GROUPE}))
    
    else:
        raise PermissionDenied()

@permission_required('ApiServer.delete_sondage')
def supprimerSondage(request, messages=[]):
    '''
        Fonction appelé quand on veut supprimer un article
    '''
    message = [{"text": "Supprimé avec succès !", "type":"success"}]
    return articles(request, message)




"""
    Section gérant tout ce qui touche aux informations
"""
@permission_required('ApiServer.view_information')
def informations(request, messages=[]):
    if GROUPE != "STUDENT":
        return render(request, 'WebServer/Gestion Affichage/Informations/index.html', exInfos("Informations", {"user_group": GROUPE}, messages))
    
    else:
        raise PermissionDenied()

@permission_required('ApiServer.add_information')
def ajouterInformation(request):
    if GROUPE != "STUDENT":
        return render(request, 'WebServer/Gestion Affichage/Informations/ajouter.html', exInfos("Modifier l'information", {"user_group": GROUPE}))
    
    else:
        raise PermissionDenied()

@permission_required('ApiServer.change_information')
def modifierInformation(request):
    if GROUPE != "STUDENT":
        if(request.GET.get("id", "") != ""):
            return render(request, 'WebServer/Gestion Affichage/Informations/modifier.html', exInfos("Modifier l'information", {"user_group": GROUPE}, informations={"title": "Le nouveaujeu", "informationContent": "je suis le contenu", "date": "2021-08-12", "type": "2"} ))

        else:
            raise Http404()

    else:
        raise PermissionDenied()

@permission_required('ApiServer.delete_information')
def supprimerInformation(request):
    return informations(request, [{"text": "Supprimé avec succés", "type":"success"}])




"""
    Section gérant tout ce qui touche aux comptes
"""
def comptes(request, messages=[]):
    return render(request, 'WebServer/Comptes/index.html', exInfos("Gestion du compte", {"user_group": GROUPE}, messages=messages))

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
                messages = [{"type": "success", "text": "Utilisateur crée avec succés"}],
            )
            return render(request, 'WebServer/Comptes/ajouter.html', informations)
            

        else:
            #Recuperation des erreurs
            messages = createErrorMessages(form)

            #Renvoie du formulaire et des erreurs
            informations = exInfos(
                pageTitle = "Ajouter un compte",
                form = form,
                messages = messages,
            )
            return render(request, 'WebServer/Comptes/ajouter.html', informations)

@login_required
def modifierCompte(request):
    #Si l'user veut modifier un compte particulier
    if request.GET.get('id', False):
        #Verification qu'il a les droits pour visionner le compte
        if request.user.has_perm("ApiServer.change_user"):
            return render(request, 'WebServer/Comptes/modifierCompteAutre.html', exInfos("Modifier un compte", informations={"prenom": "Jean Michel", "nom": "Bernadette", "email": "JMBernadette@gmail.com", "pseudo": "JMB", "image": "/static/IMG/Logo_lycée_Bourdelle.jpg"}))
        
        else: 
            return redirect("/comptes")

    else:
        if request.method == "POST":
            #Si l'user veut modifier un compte particulier
            id = request.POST.get("id")
            if id == None:
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
                            return render(request, "WebServer/Comptes/modifierComptePerso.html", exInfos("Modifier mon compte", messages=[{"type": "danger", "text": "Les mots de passes ne sont pas identiques."}]))
                        
                    #Sauvegarde du reste des informations
                    form.save()

                    #Mise à jour du cookie de session
                    update_session_auth_hash(request, request.user)

                    return render(request, "WebServer/Comptes/modifierComptePerso.html", exInfos("Modifier mon compte", messages=[{"type": "success", "text": "Compte modifié !"}]))
                
                else:
                    return render(request, "WebServer/Comptes/modifierComptePerso.html", exInfos("Modifier mon compte", messages=createErrorMessages(form)))
            
            else:
                #Modification d'un autre compte
                if request.user.has_perm("ApiServer.change_user"):
                    pass
                else:
                    return PermissionDenied()
        else:
            form = forms.changeOwnAccount(instance=request.user)
            return render(request, 'WebServer/Comptes/modifierComptePerso.html', exInfos("Modifier mon compte", form=form))

@login_required
def supprimerCompte(request):
    if request.GET.get("id", False):
        if request.user.has_perm("ApiServer.delete_user"):
            user = get_object_or_404(models.User, pk = id)

            user.is_active = False
            user.save()
            message = {"text": "Compte bien désactivé !", "type": "success"}


        else:
            return PermissionDenied()
    else:
        request.user.is_active = False
        request.user.save()
        message = {"text": "Compte bien désactivé !", "type": "success"}
    return afficherComptes(request, message)

def deconnection(request):
    logout(request)
    return redirect("/")

@permission_required('ApiServer.view_user')
def afficherComptes(request, messages=[]):
    users = models.User.objects.all()
    print(users[1].groups.all())
    return render(request, 'WebServer/Comptes/voirToutComptes.html', exInfos("Utilisateurs", messages=messages, informations={"users": users}))





"""
    Section contenant les fonctions qui servent pour les views mais que n'en retourne pas
"""
def exInfos(pageTitle, userGr={}, messages=[], informations={}, form={}):
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
        "userGr": userGr,
        "messages": messages,
        "informations": informations,
        "form": form,
    }

def createErrorMessages(form):
    '''
        Fonction créeant depuis un formulaire, une liste de message d'erreur prête à être passée aux Templates pour les
        afficher à l'utilisateur.

        @Params :
            form {ModelForm}     - Formulaire non valide

        @Return :
            list : Liste des érreurs déjà formatée pour les Templates
    '''
    errors = form.errors.as_data().values()
    messages = []
    for value in errors:
        messages.append({"type": "danger", "text": value[0].message})

    return messages

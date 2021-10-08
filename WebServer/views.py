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
import datetime


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
            #Si un mot de passe n'est pas rentré, il peut s'agir de la première connexion d'un utilisateur donc qu'il n'y a pas de mot de passe
            if password == "":
                #Essaye de trouver un utilisateur avec le même identifiant
                try:
                    user = models.User.objects.get(username=username)
                
                except models.User.DoesNotExist: #S'il ne le trouve pas
                    messages.warning(request, "Compte introuvable")
                    return render(request, "login.html")

                else: 
                    #S'il un utilisateur est trouvé et qu'il ne s'est pas encore connecté une seule fois
                    if user.password == "":
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
                            #Si 'utilisateur n'a pas de mot de passe enregistré
                            if user.password == "":
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
    articles = models.Article.objects.all()
    return render(request, 'WebServer/Articles/index.html', exInfos("Articles", informations=articles))

@permission_required('ApiServer.add_article')
def ajouterArticle(request):
    '''
        Fonction appelé quand on veut écrire un article.
    '''
    if request.method == "GET":
        form = forms.ArticleForm()
        return render(request, 'WebServer/Articles/ajouter.html', exInfos("Ajouter un article"))

    elif request.method == "POST":
        form = forms.ArticleForm(request.POST, request.FILES)

        if form.is_valid():
            record = form.save(commit=False)
            record.author = models.User.objects.filter(pk=request.user.pk)[0]
            record.last_edit_by = models.User.objects.filter(pk=request.user.pk)[0]
            
            record.save()


            messages.success(request, "Article bien ajouté !")
            return redirect("/articles/ajouter")

        else:
            createErrorMessages(request, form)
            return render(request, "WebServer/Articles/ajouter.html", exInfos("Ajouter un article", form=form))

@permission_required('ApiServer.change_article')
def modifierArticle(request):
    '''
        Fonction appelé quand on veut modifier un article.
    '''
    #To-do : Verification du groupe / utilisateur pour voir sil a le droit de modifier l'article
    id = request.GET.get("id", False)

    if request.method == "GET":
        if id:
            form = forms.ArticleForm()
            article = get_object_or_404(models.Article, pk = id)
            return render(request, 'WebServer/Articles/modifier.html', exInfos("Modifier un article", informations=article, form=form))

        else:
            raise Http404()

    elif request.method == "POST":
        #Recupération de l'article choisi
        article = get_object_or_404(models.Article, pk=id)
        form = forms.ArticleForm(request.POST, request.FILES, instance=article)

        if form.is_valid():
            form.save()

            #On modifie la dernière personne l'ayant modifié
            article.last_edit_by = request.user
            article.save()

            messages.success(request, "Article modifié avec succés !")
            return redirect("/articles/modifier?id="+id)

        else: #Il y a eu un problème
            createErrorMessages(request, form)
            return render(request, "WebServer/Articles/modifier.html", exInfos("Modifier un article", form=form, informations=article))

@permission_required('ApiServer.delete_article')
def supprimerArticle(request):
    '''
        Fonction appelé quand on veut supprimer un article
    '''
    id = request.GET.get("id", False)
    if id:
        articles = get_object_or_404(models.Article, pk = id)
        #To-do Verification du groupe
        articles.delete()
        messages.success(request, "Supprimé avec succès !")

    else:
        Http404()
    return redirect("/articles")

@permission_required('ApiServer.change_article')
def toggleVisibiliteArticle(request):
    #Vérification du groupe pour savoir si on peut modifier ou non
    id = request.GET.get("id", False)
    if id:
        article = get_object_or_404(models.Article, pk = id)
        if article.is_shown:
            article.is_shown = False

        else:
            if article.expiration_date < datetime.date.today():
                date = datetime.date.today()
                newDate = date.replace(day=date.day + 7)

                article.expiration_date = newDate

            article.is_shown = True

        article.save()
        messages.success(request, "Modifié avec succés")

    else:
        Http404()

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
    sondages = models.Survey.objects.all()
    return render(request, 'WebServer/Gestion Affichage/Sondages/index.html', exInfos("Sondages", informations=sondages))

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
    id = request.GET.get("id", "")
    if id:
        sondage = get_object_or_404(models.Survey, pk=id)
        sondage.delete()
        messages.success(request, "Sondage supprimé avec succés !")

    else:
        Http404()
    return redirect("/parametres/sondages")

@permission_required('ApiServer.change_sondage')
def toggleVisibiliteSondage(request):
    id = request.GET.get("id", "")
    if id:
        sondage = get_object_or_404(models.Survey, pk=id)
        if sondage.is_shown:
            sondage.is_shown = False
        
        else:
            if sondage.expiration_date < datetime.date.today():
                date = datetime.date.today()
                newDate = date.replace(day=date.day + 7)

                sondage.expiration_date = newDate

            sondage.is_shown = True

        sondage.save()
        
        messages.success(request, "Sondage modifié avec succés")
        return redirect("/parametres/sondages")
    
    else:
        Http404()


"""
    Section gérant tout ce qui touche aux informations
"""
@permission_required('ApiServer.view_information')
def informations(request):
    infos = models.Info.objects.all()
    return render(request, 'WebServer/Gestion Affichage/Informations/index.html', exInfos("Informations", informations=infos))

@permission_required('ApiServer.add_information')
def ajouterInformation(request):
    if request.method == "GET":
        infotypes = models.InfoType.objects.all()
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


@permission_required('ApiServer.change_information')
def modifierInformation(request):
    id = request.GET.get("id", "")
    if(id):
        info = get_object_or_404(models.Info, pk=id)

        if request.method == "GET":
            form = forms.InformationForm()
            infotypes = models.InfoType.objects.all()

            return render(request, 'WebServer/Gestion Affichage/Informations/modifier.html', exInfos("Modifier l'information", form = form, informations={"info": info, "infotypes": infotypes}))
        
        elif request.method == "POST":
            form = forms.InformationForm(request.POST, instance=info)

            if form.is_valid():
                form.save()

                messages.success(request, "Information bien mise à jour !")
                return redirect("/parametres/informations")

            else:
                createErrorMessages(request, form)
                infotypes = models.InfoType.objects.all()
                return render(request, 'WebServer/Gestion Affichage/Informations/modifier.html', exInfos("Modifier l'information", form = form, informations={"info": info, "infotypes": infotypes}))


    else:
        raise Http404()


@permission_required('ApiServer.delete_information')
def supprimerInformation(request):
    id = request.GET.get('id', '')
    if id:  
        info = get_object_or_404(models.Info, pk=id)
        info.delete()
        messages.success(request, "Supprimé avec succés")

    else:
        Http404()

    return redirect("/parametres/informations")

@permission_required('ApiServer.change_information')
def toggleVisibiliteInformation(request):
    id = request.GET.get('id', "")
    if(id):
        info = get_object_or_404(models.Info, pk=id)

        if info.is_shown:
            info.is_shown = False
            messages.success(request, "Information cachée !")

        else:
            if info.expiration_date < datetime.date.today():
                date = datetime.date.today()
                newDate = date.replace(day=date.day + 7)

                info.expiration_date = newDate

            info.is_shown = True
            messages.success(request, "Information affichée !")

        info.save()

    return redirect("/parametres/informations")




"""
    Section gérant tout ce qui touche aux comptes
"""
@login_required
def comptes(request):
    #Récuperation des articles crée par l'user
    articles = models.Article.objects.all().filter(author_id = request.user.id)
    sondages = models.Survey.objects.all().filter(author_id = request.user.id)
    return render(request, 'WebServer/Comptes/index.html', exInfos("Gestion du compte", informations={"articles": articles, "sondages": sondages}))

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
            #Si l'utilisateur est trouvé on l'affiche sinon on renvoie un 404
            user = get_object_or_404(models.User, pk=id)

            print(user.id)
            print(request.user.id)
            if user.id == request.user.id:
                return redirect("/comptes/modifier")

            articles = models.Article.objects.filter(author=user)
            sondages = models.Survey.objects.filter(author=user)

            if request.user.has_perm('ApiServer.change_user'):
                canEdit = True
            else:
                canEdit = False

            return render(request, 'WebServer/Comptes/modifierCompteAutre.html', exInfos("Modifier un compte", informations={"user": user, "articles": articles, "sondages": sondages, "canEdit": canEdit}))
            

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
    #Si l'user desactive un autre compte
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

    else: #Sinon il desactive son compte
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

@permission_required('ApiServer.change_user')
def resetPassword(request):
    id = request.GET.get("id", "")

    if id:
        user = get_object_or_404(models.User, pk = id)

        user.password = ""

        user.save()

        messages.success(request, "Mot de passe réinitialisé avec succés")

    return redirect("/comptes/voir")


"""
    Section gérant tout ce qui touche aux écrans
"""
def ajouterEcran(request):
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
    

def modifierEcran(request):
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
        Http404()


def supprimerEcran(request):
    return redirect("/parametres")


def ajouterPage(request):
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
    

def modifierPage(request):
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
        Http404()

def supprimerPage(request):
    return redirect("/parametres")

def modifierAffectation(request):
    """
        Fonction s'occupant de renvoyer la page qui permet d'affecter chaque écran à une page
    """
    if request.method == "GET":
        ecrans = models.Display.objects.all().order_by("name")
        pages = models.Page.objects.all()
        return render(request, 'WebServer/Gestion Affichage/Ecrans/modifierLaffectation.html', exInfos("Modification des écrans", informations={"ecrans": ecrans, "pages": pages}))
    
    elif request.method == "POST":
        #Si l'user fourni une page précise, on le recupère sinon on met la page par defaut (correspondant au -1 pour l'identifiant)
        pageId = int(request.POST.get("page", -1))
        
        #Si l'id fourni est différent de -1 donc que l'user l'a fourni
        if pageId > -1:
            #Recherche de la page correspondante
            page = models.Page.objects.filter(pk = pageId)

        #Si l'user a donné une liste d'écrans à modifier
        if request.POST.getlist("ecrans", ""):

            #Pour tous les écrans dans cette liste
            for i in range(len(request.POST.getlist("ecrans"))):
                #Id de l'écran qu'on modifie dans cette itération
                ecranId = request.POST.getlist("ecrans")[i]

                #L'écran correspondant à l'id
                ecran = models.Display.objects.filter(pk = ecranId)

                #Si l'écran n'est pas trouvé
                if len(ecran) < 1:
                    messages.error(request, "Il y a eu un problème, l'écran avec l'identifiant " + ecranId + " n'a pas pu être mis à jour")
                
                #S'il est trouvé
                else:
                    #Si on a pas trouvé la page ou que l'user ne souhaite pas de page en particulier
                    if pageId == -1:
                        ecran[0].page = None

                    #Si l'user veut une page en particulier qu'on a trouvé
                    else:
                        ecran[0].page = page[0]

                    #Sauvegarde
                    ecran[0].save()

            messages.success(request, "Les écrans ont bien été mis à jour !")

        
        return redirect("/parametres/modifierPageEcran")


"""
    Section contenant les fonctions qui servent pour les views mais que n'en retourne pas
"""
def exInfos(pageTitle, informations={}, form={}):
    '''
        Fonction appelé quand on veut envoyer des données complémentaires aux Templates comme par exemple le groupe 
        de l'utilisateur ou un message d'information sur une action effectuée

        @Params :
            pageTitle {string}     - Nom de la page
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
    print(form.errors)
    errors = form.errors.as_data().values()
    for value in errors:
        messages.error(request, value[0].message)

import requests
from .keys import *
from .models import Pronote, Repas, Aliment, PartieDuRepas, ProfAbsent
import datetime

timeBetweenTwoGenerationToken = 60 * 24
timeBetweenTwoQueries = 1

def canQueryAgain():
    """
        Fonction s'occupant de savoir si on peut refaire une requète à pronote ou s'il faut attendre 
        Renvoie True quand on peut se reconnecter et False quand on ne peut pas 
    """
    #Récupération de la dernière connexion à pronote si forToken est vraie, sinon recupération de la dernière requete faite à pronote
    lastPronoteConnection = Pronote.objects.latest('last_token_query')

    #Calcul de la dernière heure avant de pouvoir faire une requete (l'heure actuelle - le temps entre 2 requetes)
    timeBeforeNewQuery = datetime.datetime.now(datetime.timezone.utc)

    day = timeBeforeNewQuery.day

    day -= 1
    month = timeBeforeNewQuery.month

    if day < 0:
        day += 30
        month -= 1

    timeBeforeNewQuery = timeBeforeNewQuery.replace(day = day, month = month)

    return lastPronoteConnection.last_query < timeBeforeNewQuery

def createNewToken():
    #Récupération des informations du compte pour la connexion
    data = {
        "url": PRONOTE_URL,
        "username": PRONOTE_USERNAME,
        "password": PRONOTE_PASSWORD,
        "cas": PRONOTE_CAS
    }

    newPronoteToken = Pronote()
    newPronoteToken.save()

    #Connexion
    requete = requests.post("http://127.0.0.1:21727/auth/login", json=data)
    print("Connection to Pronote")
    print("Result : {}\n".format(requete.json()))


    #Si tout s'est bien passé, on enregistre et retourne le token fraichement obtenu 
    if requete.status_code == 200:
        token = requete.json()["token"]

        newPronoteToken.token = token
        newPronoteToken.save()

        #Défini la connexion comme une connexion à ne pas fermer 
        headers = {
            'Content-type': 'application/json',
            'Token': token,
        }

        query = {
            'query': 'mutation {setKeepAlive(enabled: true)} query {menu(from: "2021-10-05"){date, meals{name}},timetable(from: "2021-10-05"){status, teacher, from, to}}'
        }

        requete = requests.post("http://127.0.0.1:21727/graphql", headers=headers, json=query)
        print("Setting keepAlive mutation for the pronote server")
        print("Result : {}\n".format(requete.json()))

        return token

def loginToPronote():
    """
        Fonction s'occupant de se connecter à pronote et de renvoyer le token à utiliser pour les requètes
    """

    #Récupération de la dernière connexion à pronote
    lastPronoteConnection = Pronote.objects.latest('last_token_query')

    #Si la dernière connexion à pronote était il y a trop longtemps, on peut récupérer un nouveau token
    if canQueryAgain():
        return createNewToken()

    else: #Sinon on renvoie le token qu'on à utilisé dans la dernière requète 
        return lastPronoteConnection.token


def refreshInfos(isRecursive = False):
    """
        Fonction rafraichissant les informations de pronote dans la bdd
        Le paramètre isRecursive permet de bloquer la création de token Pronote à l'infini s'il y a un problème
        avec la requète. 
    """
    #Récupération du token pour la connexion à pronote
    token = loginToPronote()

    print("Token used : {}".format(token))

    #Formatage de la date pour que pronote comprenne que veuilles le menu d'aujourd'hui
    date = datetime.datetime.now()
    date = date.replace(day=date.day - 1)

    #Commande que l'on envoie au serveur qui récupère les menus (midi - soir) à la date d'aujourd'hui
    #Dans la requete on demande le menu et l'emploi du temps 
    """
        query {
            menu(from: "2021-10-05") {
                date, 
                meals {
                    name
                }
            },
            timetable(from: "2021-10-05") {
                status, 
                teacher, 
                from, 
                to
            }
        }
    """
    headers = {
        'Content-type': 'application/json',
        'Token': token,
    }
    

    query = {
        "query": '{menu(from: "' + date.isoformat() + '"){date, meals{name}},timetable(from: "' + date.isoformat() + '"){status, teacher, from, to}}'
    }

    #Envoie de la requète vers pronote
    requete = requests.post("http://127.0.0.1:21727/graphql", headers=headers, json=query)
    print("Getting informations from Pronote")
    print("Result : {}\n".format(requete.json()))

    #Mise à jour de la date de la dernière requète
    last_query = Pronote.objects.latest("last_query")
    last_query.last_query = datetime.datetime.now(tz = datetime.timezone.utc)
    last_query.save()

    #Si le token n'est plus valide
    if "errors" in requete.json() and requete.json()["errors"][0]["message"].split("code: ")[1].split(",")[0] == "5":
        #Vérification que l'on a pas déjà appelé la fonction pour ne pas créer des tokens à l'infini
        if not isRecursive:
            createNewToken()
            refreshInfos(True)

    #Parsing des données reçu
    elif requete.status_code == 200:
        #Si la requète nous renvoie bien un menu (ce qu'elle ne fait pas si on est Samedi par exemple)
        # car le samedi il n'y a pas de self
        if len(requete.json()["data"]) > 0:
            menus = requete.json()["data"]["menu"]

            edt = requete.json()["data"]["timetable"]

            #Si on a au moins 1 menu à ajouter
            if len(menus) > 0:
                ajoutMenus(menus)

            #Si on a un emploi du temps à traiter
            if len(edt) > 0:
                ajoutProfsAbsents(edt)

    #S'il y a un problème avec le token (Généralement l'expiration du token)
    elif requete.status_code == 500:
        #Vérification que l'on a pas déjà appelé la fonction pour ne pas créer des tokens à l'infini
        if not isRecursive:
            createNewToken()
            refreshInfos(True)    


def ajoutMenus(menus):
    """
        Fonction ajoutant les menus passés en paramètre à la bdd 
    """
    #Pour chaque menu d'aujourd'hui
    for IDMenu in range(len(menus[0]["meals"])):
        menu = menus[0]["meals"][IDMenu]

        #On sait que le premier menu est le menu du midi, or le premier index d'une liste est 0
        # Donc 0 est divisible par 2 donc la condition est vraie (et cest le menu du midi) sinon la condition
        # est fausse donc ce n'est pas le menu du midi, cest à dire que c'est celui du soir
        isRepasMidi = IDMenu % 2 == 0

        #Convertion de la date donnée par pronote(Epoch?) en une date compréhensible par la BDD 
        dateToday = convertionDatePronoteVersDatetime(menus[0]["date"]+ 2 * 3600 * 1000)

        #Vérification que le repas n'existe pas déjà dans la BDD
        repasObjects = Repas.objects.filter(repas_midi = isRepasMidi, date = dateToday)

        repas = None

        #Si on ne trouve pas de repas à la même date dans la bdd
        if len(repasObjects) == 0:
            #Initialisation du nouvel objet Repas
            repas = Repas()
            repas.repas_midi = isRepasMidi
            repas.date = dateToday
            repas.save()

        else: #Il y a deja un repas à la même date 
            # On utilise ce repas que l'on vide de tout aliment pour pouvoir les réattribuer si
            #  on a changé la composition du repas à la dernière minute 
            repas = repasObjects[0]
            repas.aliments_du_repas.clear()

        #Pour chaque partie de repas (Entrée, Viande, Dessert, etc)
        for IDpartieRepas in range(len(menu)):

            #Pour chaque Aliment dans cette partie
            for aliment in menu[IDpartieRepas]:
                #Vérification qu'il n'y ait pas déjà l'aliment dans la BDD avec le même nom et la même partie du repas
                alimentObjects = Aliment.objects.filter(name = aliment["name"], partie_du_repas = IDpartieRepas + 1)

                #S'il n'y en a pas dans la bdd
                if len(alimentObjects) == 0:
                    #On crée un nouvel aliment 
                    currentAliment = Aliment()
                    currentAliment.name = aliment["name"]
                    currentAliment.partie_du_repas = PartieDuRepas.objects.get(pk=IDpartieRepas+1)
                    currentAliment.save()

                    #Et on l'ajoute au repas que l'on est en train de construire
                    repas.aliments_du_repas.add(currentAliment)
                
                else: #S'il existe déjà dans la bdd 
                    #On l'ajoute simplement au repas que l'on est en train de construire
                    repas.aliments_du_repas.add(alimentObjects[0])

        #Sauvegarde dans la base de données
        repas.save()

def ajoutProfsAbsents(edt):
    """
        Fonction ajoutant les profs absents dans la base de donnée à partir 
        d'une liste de cours
    """
    #Pour chaque cours
    for cours in edt:
        #Si le profs et absents du cours
        if cours["status"] == "Prof. absent":
            #Convertion des temps vers une date compréhensible par la bdd
            debut = convertionDatePronoteVersDatetime(cours["from"])
            fin = convertionDatePronoteVersDatetime(cours["to"])

            #Vérification que la ligne n'a pas déjà été ajouté avant
            queryProfAbs = ProfAbsent.objects.filter(teacher = cours["teacher"], debut = debut, fin = fin)

            #Si l'absence n'est pas dans la bdd
            if len(queryProfAbs) == 0:
                #On l'ajoute
                absence = ProfAbsent()
                absence.teacher = cours["teacher"]
                absence.debut = debut
                absence.fin = fin
                absence.save()

def convertionDatePronoteVersDatetime(epoch):
    """
        Converti un nombre de milliseconde en une date compréhensible par python et la bdd
    """
    return datetime.datetime.fromtimestamp(epoch/1000, tz=datetime.timezone.utc)
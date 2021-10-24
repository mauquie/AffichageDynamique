import requests
from .keys import *
from .models import Pronote, Repas, Aliment, PartieDuRepas
import datetime

timeBetweenTwoGenerationToken = 60
timeBetweenTwoQueries = 30

def canQueryAgain(forToken=True):
    """
        Fonction s'occupant de savoir si on peut refaire une requète à pronote ou s'il faut attendre 
        Renvoie True quand on peut se reconnecter et False quand on ne peut pas 
    """
    #Récupération de la dernière connexion à pronote
    lastPronoteConnection = Pronote.objects.latest('last_query')

    #Calcul de la dernière heure avant de pouvoir faire une requete (l'heure actuelle - le temps entre 2 requetes)
    timeBeforeNewQuery = datetime.datetime.now(datetime.timezone.utc)

    minute = timeBeforeNewQuery.minute

    #Si on veut calculer le temps avant la prochaine fois que l'on récupère un token
    if forToken:
        minute -= timeBetweenTwoGenerationToken 

    else: #Ou si on veut simplement faire une nouvelle requète pour avoir de nouvelles informations
        minute -= timeBetweenTwoQueries

    hour = timeBeforeNewQuery.hour

    #Si on a des minutes négatives, on enleve 1 heure (Logique)
    if minute < 0:
        minute = minute + 60
        hour = hour - 1

    timeBeforeNewQuery = timeBeforeNewQuery.replace(minute = minute, hour = hour)

    return lastPronoteConnection.last_query < timeBeforeNewQuery


def loginToPronote():
    """
        Fonction s'occupant de se connecter à pronote et de renvoyer le token à utiliser pour les requètes
    """

    #Récupération de la dernière connexion à pronote
    lastPronoteConnection = Pronote.objects.latest('last_query')

    #Si la dernière connexion à pronote était il y a trop longtemps, on peut récupérer un nouveau token
    if canQueryAgain(True):
        #Récupération des informations du compte pour la connexion
        data = {
            "url": PRONOTE_URL,
            "username": PRONOTE_USERNAME,
            "password": PRONOTE_PASSWORD,
            "cas": PRONOTE_CAS
        }

        #Connexion
        requete = requests.post("http://127.0.0.1:21727/auth/login", json=data)
        print("Connection to Pronote")


        #Si tout s'est bien passé, on enregistre et retourne le token fraichement obtenu 
        if requete.status_code == 200:
            token = requete.json()["token"]

            newPronoteToken = Pronote()
            newPronoteToken.token = token
            newPronoteToken.save()

            return token

    else: #Sinon on renvoie le token qu'on à utilisé dans la dernière requète 
        return lastPronoteConnection.token


def refreshMenu():
    #Si on peut refaire un requète vers pronote (garde-fou pour évité le ban-ip)
    if canQueryAgain(False):
        #Récupération du token pour la connexion à pronote
        token = loginToPronote()

        #Formatage de la date pour que pronote comprenne que veuilles le menu d'aujourd'hui
        date = datetime.datetime.now()
        date = date.replace(day=date.day - 1)

        #Commande que l'on envoie au serveur qui récupère les menus (midi - soir) à la date d'aujourd'hui
        query = {"query": '{menu(from: "' + date.strftime("%Y-%m-%d") + '"){date, meals{name}}}'}

        headers = {
            'Content-type': 'application/json',
            'Token': token,
        }

        #Envoie de la requète vers pronote
        requete = requests.post("http://127.0.0.1:21727/graphql", headers=headers, json=query)
        print("Getting menu from Pronote")

        #Parsing des données reçu
        if requete.status_code == 200:
            #Si la requète nous renvoie bien un menu (ce qu'elle ne fait pas si on est Samedi par exemple)
            # car le samedi il n'y a pas de self
            if len(requete.json()["data"] > 0):
                menus = requete.json()["data"]["menu"][0]

                #Pour chaque menu d'aujourd'hui
                for IDMenu in range(len(menus["meals"])):
                    menu = menus["meals"][IDMenu]

                    #On sait que le premier menu est le menu du midi, or le premier index d'une liste est 0
                    # Donc 0 est divisible par 2 donc la condition est vraie (et cest le menu du midi) sinon la condition
                    # est fausse donc ce n'est pas le menu du midi, cest à dire que c'est celui du soir
                    isRepasMidi = IDMenu % 2 == 0

                    #Convertion de la date donnée par pronote(Epoch?) en une date compréhensible par la BDD 
                    dateToday = datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=menus["date"]/1000 + 7200)


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

        
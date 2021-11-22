import requests
from .models import Repas, Aliment, PartieDuRepas, ProfAbsent
import datetime
import pytz

def refreshMenus():
    """
        Fonction s'occupant de rafraichir les données du menu du jour dans la base de données au cas ou il ait changé
    """
    #Requete à pronote
    requete = requests.get("http://127.0.0.1:5000/menus")

    #S'il nous renvoie des données alors on va les traiter
    if len(requete.json()["data"]) > 0:
        menus = requete.json()["data"]

        ajoutMenus(menus)

def refreshProfs():
    #Requete à pronote
    requete = requests.get("http://127.0.0.1:5000/edt")
    
    #S'il nous renvoie des données alors on va les traiter
    if len(requete.json()["data"]) > 0:
        edt = requete.json()["data"]

        ajoutProfsAbsents(edt)


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
        dateToday = convertionDatePronoteVersDatetime(menus[0]["date"])

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
        if "status" in cours and cours["status"] == "Prof. absent" and cours["hasDuplicate"] == False:
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

def convertionDatePronoteVersDatetime(dateG):
    """
        Converti un string sous la forme "2021-10-05T09:25:00.000Z" en une date compréhensible par python et la bdd
    """
    #Récupération du décalage horaire en secondes 
    offset = int(datetime.datetime.now(pytz.timezone('Europe/Paris')).strftime('%z')[2])*3600

    #Formatage de la date donnée (string) en datetime compréhensible par python
    date = datetime.datetime.strptime(dateG, "%Y-%m-%dT%H:%M:%S.%fZ")
    
    #Ajout du décalage horaire au nombre de secondes total pour obtenir la date donnée
    date = datetime.datetime.utcfromtimestamp(date.timestamp() + offset)

    return date
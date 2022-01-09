import requests
from .models import Meals, Foods, MealParts, Absents, Teachers
import datetime
import pytz

def refreshMenus():
    """
        Fonction s'occupant de rafraichir les données du menu du jour dans la base de données au cas ou il ait changé
    """
    # Requete à pronote
    try:
        requete = requests.get("http://127.0.0.1:5000/menus")

    except requests.ConnectionError:
        print("Impossible connection to pronoteServer, check if it's on.")

    else:
        # S'il nous renvoie des données alors on va les traiter
        if len(requete.json()["data"]) > 0:
            menus = requete.json()["data"]

            ajoutMenus(menus)

def refreshProfs():
    """
        Fonction s'occupant de rafraichir les données des profs absents du jour dans la base de données au cas ou ils aient changé
    """
    # Requete à pronote
    try:
        requete = requests.get("http://127.0.0.1:5000/edt")
    
    except requests.ConnectionError:
        print("Impossible connection to pronoteServer, check if it's on.")

    else:
        # S'il nous renvoie des données alors on va les traiter
        if len(requete.json()["data"]) > 0:
            edt = requete.json()["data"]

            ajoutProfsAbsents(edt)


def ajoutMenus(meals):
    """
        Fonction ajoutant les menus passés en paramètre à la bdd 
    """
    # Pour chaque menu d'aujourd'hui
    for IDMeal in range(len(meals[0]["meals"])):
        meal = meals[0]["meals"][IDMeal]

        # On sait que le premier menu est le menu du midi, or le premier index d'une liste est 0
        #  Donc 0 est divisible par 2 donc la condition est vraie (et cest le menu du midi) sinon la condition
        #  est fausse donc ce n'est pas le menu du midi, cest à dire que c'est celui du soir
        isMiddayMeal = IDMeal % 2 == 0

        # Convertion de la date donnée par pronote(Epoch?) en une date compréhensible par la BDD 
        dateToday = convertionDatePronoteVersDatetime(meals[0]["date"])

        # Vérification que le repas n'existe pas déjà dans la BDD
        mealsObjects = Meals.objects.filter(is_midday = isMiddayMeal, date = dateToday)

        mealObject = None

        # Si on ne trouve pas de repas à la même date dans la bdd
        if len(mealsObjects) == 0:
            # Initialisation du nouvel objet Repas
            mealObject = Meals()
            mealObject.is_midday = isMiddayMeal
            mealObject.date = dateToday
            mealObject.save()

        else: # Il y a deja un repas à la même date 
            #  On utilise ce repas que l'on vide de tout aliment pour pouvoir les réattribuer si
            #   on a changé la composition du repas à la dernière minute 
            mealObject = mealsObjects[0]
            mealObject.to_eat.clear()

        # Pour chaque partie de repas (Entrée, Viande, Dessert, etc)
        for IDMealPart in range(len(meal)):

            # Pour chaque Aliment dans cette partie
            for food in meal[IDMealPart]:
                # Vérification qu'il n'y ait pas déjà l'aliment dans la BDD avec le même nom et la même partie du repas
                foodObjects = Foods.objects.filter(name = food["name"], meal_part = IDMealPart + 1)

                # S'il n'y en a pas dans la bdd
                if len(foodObjects) == 0:
                    # On crée un nouvel aliment 
                    currentFood = Foods()
                    currentFood.name = food["name"]
                    currentFood.meal_part = MealParts.objects.get(pk=IDMealPart+1)
                    currentFood.save()

                    # Et on l'ajoute au repas que l'on est en train de construire
                    mealObject.to_eat.add(currentFood)
                
                else: # S'il existe déjà dans la bdd 
                    # On l'ajoute simplement au repas que l'on est en train de construire
                    mealObject.to_eat.add(foodObjects[0])

        # Sauvegarde dans la base de données
        mealObject.save()
        
def ajoutProfsAbsents(edt):
    """
        Fonction ajoutant les profs absents dans la base de donnée à partir 
        d'une liste de cours
    """
    # Pour chaque cours
    for cours in edt:
        # Si le profs et absents du cours
        if "status" in cours and cours["status"] == "Prof. absent" and cours["hasDuplicate"] == False:
            # Convertion des temps vers une date compréhensible par la bdd
            start = convertionDatePronoteVersDatetime(cours["from"])
            end = convertionDatePronoteVersDatetime(cours["to"])

            # Recherche du prof dans la BDD sinon on l'ajoute
            teacher = Teachers.objects.get_or_create(name=cours["teacher"])[0]
            teacher.save()

            # Recherche d'une absence déjà notée possible (pour éviter les doublons)
            queryProfAbs = Absents.objects.filter(teacher = teacher.id, date_start = start, date_end = end)

            # Si l'absence n'est pas déjàdans la bdd
            print(queryProfAbs)
            if len(queryProfAbs) == 0:
                # On l'ajoute
                absence = Absents()
                absence.teacher = teacher
                absence.date_start = start
                absence.date_end = end
                absence.save()

def convertionDatePronoteVersDatetime(dateG):
    """
        Converti un string sous la forme "2021-10-05T09:25:00.000Z" en une date compréhensible par python et la bdd
    """
    # Récupération du décalage horaire en secondes 
    offset = int(datetime.datetime.now(pytz.timezone('Europe/Paris')).strftime('%z')[2])*3600

    # Formatage de la date donnée (string) en datetime compréhensible par python
    date = datetime.datetime.strptime(dateG, "%Y-%m-%dT%H:%M:%S.%fZ")
    
    # Ajout du décalage horaire au nombre de secondes total pour obtenir la date donnée
    date = datetime.datetime.utcfromtimestamp(date.timestamp() + offset)

    return date
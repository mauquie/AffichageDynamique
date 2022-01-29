#
#  Created by Elowarp on 19/12/2021
#

"""
Gère toute la partie "météo" du projet
"""

import requests
import datetime
import AffichageDynamique.settings as settings

class MeteoGetter:
    """
    Classe s'occupant de récupérer les données de l'api openweatherapi 
    et de les retournées quand elles sont demandées tout en garantissant 
    de ne pas se faire bannir de l'api à cause du nombre d'appel de l'api

    Attributes:
        lastData (dict): Dernières données récupérées via l'api
        didFirstFetch (bool): Vérifie si le premier fetch a été fait
            Si non, le serveur vient de s'être lancé dans on peut
            fetch l'api sans risquer d'atteindre la limite

            Si oui, le serveur est déjà lancé et la requête vers l'api a
            déjà été faite donc on attend au moins 1h avant de re fetch
        lastQuery (datetime): Dernière heure à laquelle on a récupéré les 
            données

    """
    def __init__(self):
        #Récupération de l'heure + data actuelle mais en enlevant les minutes
        self._apiKey = settings.METEO_TOKEN
        self.lastData = {}

        self.didFirstFetch = False

        self.lastQuery = datetime.datetime.now()
        self.lastQuery = self.lastQuery.timestamp() - (self.lastQuery.minute * 60)

    def _canQuery(self):
        """
        Vérification qu'on peut faire la mise à jour des données
        Sans arriver à la limite d'appel de l'api à la fin du mois 
        (Ce qui revient à 1 appel toutes les heures)
        """

        #Vérification de la différence de temps entre la dernière fois qu'on a get et mtn
        diff = datetime.datetime.now().timestamp() - self.lastQuery

        if(diff > 60 * 60): #1 Requete toutes les 60 minutes
            return True

        return False

    def _fetchMeteo(self):
        """
        Récupère les données depuis l'api de `OpenWeatherMap <https://openweathermap.org/api/one-call-api>`_
        """

        #Mise à jour de la derniere date où on a recup les data
        self.lastQuery = datetime.datetime.now().timestamp()
        
        print("Getting weather's data")
        meteoRes = requests.get("http://api.openweathermap.org/data/2.5/onecall?lat=44.0833&lon=1.5&exclude=current,minutely&units=metric&appid=" + self._apiKey)
        
        #Traitement des données pour seulement garder celles nécessaires
        hoursData = meteoRes.json()["hourly"]
        hourly = [
            {
                "dt": hour["dt"],
                "temp": hour["temp"],
                "feels_like": hour["feels_like"],
                "weather": hour["weather"],
                
            }
            for hour in hoursData
        ]

        todayData = meteoRes.json()["daily"][0]
        today = {
            "dt": todayData["dt"],
            "temp": todayData["temp"],
            "feels_like": todayData["feels_like"],
            "weather": todayData["weather"],
        }

        #Mise à jour des données de la classe
        self.lastData = {
            "hourly": hourly,
            "today": today
        }
    
    def getMeteoData(self):
        """
        Renvoie les dernière données récupérées, si :py:meth:`_canQuery` nous autorise
        alors on va refaire une demande à l'api pour mettre à jour les infos, sinon
        on prend les dernières stockées dans :py:attr:`lastData`
        """
        #Méthode s'occupant de renvoyer les données qd elles sont demandées par les écrans
        if self._canQuery() or not self.didFirstFetch:
            self.didFirstFetch = True
            self._fetchMeteo()

        return self.lastData	
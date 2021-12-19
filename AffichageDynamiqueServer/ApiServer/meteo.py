#
#  Created by Elowarp on 19/12/2021
#
#  Classe s'occupant de gérer la météo des écrans
#


import requests
import datetime

class MeteoGetter:
    """
        Classe s'occupant de récupérer les données de l'api openweatherapi 
        et de les retournées quand elles sont demandées tout en garantissant 
        de ne pas se faire bannir de l'api à cause du nombre d'appel de l'api
    """
    def __init__(self):
        #Récupération de l'heure + data actuelle mais en enlevant les minutes
        self.lastQuery = datetime.datetime.now()
        self.lastQuery = self.lastQuery.timestamp() - (self.lastQuery.minute * 60)

        self.apiKey = "ad46a56c32405526362b69fed3971632"
        self.lastData = {}

        self._fetchMeteo() #Récupération des données pour éviter d'attendre 55mn

    def _canQuery(self):
        # Vérification qu'on peut faire la mise à jour des données
        # Sans arriver à la limite d'appel de l'api à la fin du mois 
        # (Ce qui revient à 1 appel toutes les heures)

        #Vérification de la différence de temps entre la dernière fois qu'on a get et mtn
        diff = datetime.datetime.now() - self.lastQuery
        
        if(diff.seconds > 60 * 60): #1 Requete toutes les 60 minutes
            return True

    def _fetchMeteo(self):
        #Récupération des données depuis l'api de openweatherapi

        #Mise à jour de la derniere date où on a recup les data
        self.lastQuery = datetime.datetime.now()
        
        print("Getting weather's data")
        meteoRes = requests.get("http://api.openweathermap.org/data/2.5/onecall?lat=44.0833&lon=1.5&exclude=daily,minutely&units=metric&appid=" + self.apiKey)
        
        #Mise à jour des données de la classe
        self.lastData = {"data": meteoRes.json()["hourly"]}
    
    def getMeteoData(self):
        #Méthode s'occupant de renvoyer les données qd elles sont demandées par les écrans
        if self._canQuery():
            self._fetchMeteo()

        return self.lastData	
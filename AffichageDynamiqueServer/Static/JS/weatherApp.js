/**
 * Created by Elowarp on 19/12/2021
 * 
 * Fichier qui s'occupe de toute la partie météo frontend en JS
 */

class WeatherApp{
    /**
     * Classe gérant ce qui touche à la météo, la bar météo et le widget météo en bas de l'écran
     * 
     * Pour l'utiliser il suffit juste de créer une instance et ensuite il s'occupe de se mettre à jour seul
     */
    constructor(){
        this.data = {}
        this.todaysWeather = {}

        //Dictionnaire contenant les liens vers les images (jour) correspondant à la météo
        this.weatherDayIcons = {
            "01": "sun--v2.png",
            "02": "partly-cloudy-day--v2.png",
            "03": "cloud.png",
            "04": "cloud.png",
            "10": "partly-cloudy-rain--v2.png",
            "09": "rain--v2.png",
            "11": "cloud-lighting--v2.png",
            "13": "snow.png",
            "50": "fog-night--v2.png"
        }

        //Dictionnaire contenant les liens vers les images (nuit) correspondant à la météo
        this.weatherNightIcons = {
            "01": "bright-moon--v2.png",
            "02": "partly-cloudy-night--v1.png",
            "03": "cloud.png",
            "04": "cloud.png",
            "10": "rainy-night.png",
            "09": "rain--v2.png",
            "11": "cloud-lighting--v2.png",
            "13": "snow.png",
            "50": "fog-night--v1.png"
        }

        //création dictionnaire liant météo et texte
        this.dictTextMeteo = {
            "01": "rayonnante !",
            "02": "nuageuse",
            "03": "nuageuse",
            "04": "nuageuse",
            "10": "pluvieuse malheureusement",
            "09": "déluvienne, sortez vos parapluies !",
            "11": "orageuse malheureusement",
            "13": "enneigée brrrrrrr",
            "50": "brumeuse malheureusement"
        }
        //création dictionnaire liant météo et couleur
        this.dictColourMeteo = {
            "01": "red",
            "02": "gray",
            "03": "gray",
            "04": "gray",
            "10": "blue",
            "09": "dark-blue",
            "11": "yellow",
            "13": "white",
            "50": "gray",
        }

        //Appel des fonctions de création de la bar météo et du création du widget
        this._createWeatherBar()
        this._createWeatherWidget()
        this._addMeteoText()

        setInterval(() => {
            this._createWeatherBar()
            this._createWeatherWidget()
            this._addMeteoText()
            console.log("reload meteo")
        }, 1000 * 60) // Toutes les minutes
    }

    _createWeatherBar(){
        /**
         * Création de la bar météo qui affiche 5 cartes pour les 5 prochaines heures
         */

        //Récupération des données
        this._getData().then(() => {
            //Vidage de la bar si elle a déjà été remplie
            let cardList = document.getElementById("weatherCardList")
            cardList.innerHTML = ""

            //Pour toutes les heures à partir de maintenant et pour les 5 prochaines heures
            for (let i = 0; i < 5; i++) {
                //On prend la prevision pour l'heure i
                let hour = this.data[i]

                //Et l'heure de l'heure i
                let date = new Date(hour.dt * 1000);

                //Récupération de la tempéature
                let temp = Math.round(hour.feels_like)

                //Récupération de l'heure
                let time = date.getHours() + ":00"

                //Image correspondante à la météo
                let imgLink = this._imageWeather(hour.weather[0].description, hour.weather[0].icon)

                //Ajout de la carte correspondante
                this._addCard(temp, time, imgLink)
            }
        })
    }

    async _getData(){
        /**
         * Fonction asynchrone récupérant les données depuis notre api
         */
        await fetch("/api/meteo")
            .then(response => {
                return response.json();
            })
            .catch(err => {
                console.error(err);
            })
            .then(data => {
                this.data = data["hourly"]
                this.todaysWeather = data["today"]
            })
    }

    _imageWeather(weatherDescription, icon){
        /**
         * Fonction retournant la bonne image dépendant de la description donnée
         * 
         * @param weatherDescription {string} - Description de la météo
         * @param icon {string} - Chaine de caractère donnée correspondante à l'icone de la météo
         * 
         * @returns string - Url de l'icone correspondante
         */
        if (icon.includes("n")){
            return `https://img.icons8.com/ios-glyphs/60/000000/${this.weatherNightIcons[this._getIconNumber(icon)]}`
        
        } else {
            return `https://img.icons8.com/ios-glyphs/60/000000/${this.weatherDayIcons[this._getIconNumber(icon)]}`
        }
    }

    _getIconNumber(icon){
        /**
         * Fonction retournant le nombre correspondant à l'icone donnée par l'API
         * 
         * @param icon {string} - Chaine de caractère donnée correspondante à l'icone de la météo (ex : 01n.png)
         * 
         * @returns string - Chaine de caractère des nombres donnés par icon (ex: 01)
         */
        return [icon[0], icon[1]].join("")
    }

    _createWeatherWidget(){
        /**
         * Création du widget météo en bas à droite de l'écran
         */
        //Récupération des données
        this._getData().then(() => {
            //On prend l'heure actuelle
            let data = this.data[0]

            //Image correspondante à la météo
            let imgLink = this._imageWeather(data.weather[0].description, data.weather[0].icon)

            //Ajoute l'image au widget
            var domImage = document.getElementById("weatherImage")

            domImage.src = imgLink
        })
    }

    _addMeteoText(){
        /**
         * Ajout du texte lié à la météo dans l'article par défaut
         */
        //Récupération du texte à colorer
        this._getData().then(() => {
            //Récupération du texte lié à la météo
            let meteoText = document.getElementById("text-meteo")

            //Récupération de la moyenne météorologique du jour
            let weatherIcon = this._getIconNumber(this.todaysWeather.weather[0].icon)
            
            //Modification du texte et de sa couleur lié à la météo dans l'article par défaut
            meteoText.innerText = this.dictTextMeteo[weatherIcon]
            meteoText.style.color = this.dictColourMeteo[weatherIcon]
        })
    }



    _addCard(temp, time, imgLink){
        /**
         * Ajout d'une carte dans la bar météo
         */
        //Récupération de la liste de carte
        const cardList = document.getElementById("weatherCardList")

        let tempClass

        //Ajout d'un style à la température quand il fait trop froid ou trop chaud
        if (temp <= 10) {
            tempClass = "tempCold"

        } else if (temp >= 28) {
            tempClass = "tempHot"

        } else {
            tempClass = ""
        }

        temp = temp + "°C"

        //Ajout d'une carte correspondante à une heure
        cardList.innerHTML += `\
            <div class="col-2 mx-2 weatherCard text-center">
                <span class="d-flex justify-content-center" style="font-size: 5vh">${time}</span>
                <hr>
                <img class="my-2" src="${imgLink}" alt="" style="width: 6vh; opacity: 0.8">
                <hr>
                <span class="d-flex justify-content-center ${tempClass}" style="font-size: 5vh">${temp}</span>
            </div>
        `
    }

    getTodaysWeather(){
        /**
         * Retourne la météo moyenne de la journée
         * 
         * @returns {dict} - Météo d'aujourd'hui
         */
        return this.todaysWeather
    }
}
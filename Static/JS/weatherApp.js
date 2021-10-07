var nbCardsShown = 0 //Compte le nombre de carte affiché pour ne pas dépasser la limite de l'écran

function getWeatherInfos() {
    //Récupération des informations de l'api pour la météo
    fetch("http://api.weatherapi.com/v1/forecast.json?key=30349e9636cc4e749c5203053210310&q=Montauban&days=2&aqi=no&alerts=no", {
            "method": "GET",
            "headers": {
                "Content-type": "application/json",
                "Access-Control-Allow-Headers": "*"
            }
        })
        .then(response => {
            return response.json();
        })
        .catch(err => {
            console.error(err);
        })
        .then(data => {
            let cardList = document.getElementById("weatherCardList")
            cardList.innerHTML = ""
            nbCardsShown = 0

            var currentHour = new Date().getHours()

            //Pour les 12 prochaines heures on va afficher une carte
            for (let jour = 0; jour < 2; jour++) {
                //Si on est aujourd'hui on commence à partir de l'heure actuelle
                if (jour == 0) {
                    currentHour = new Date().getHours()

                    //Sinon on commence à partir de 00:00
                } else {
                    currentHour = 0

                }

                //Pour toutes les heures à partir de currentHour jusque la fin de la liste
                for (let i = currentHour; i < data.forecast.forecastday[jour].hour.length; i++) {
                    //Si on a déjà 12 cartes affichées on coupe la boucle
                    if (nbCardsShown == 12) {
                        break;

                    } else if (nbCardsShown == 0) {
                        //On prend la température actuelle
                        hour = data.current

                        //Et l'heure actuelle
                        var date = new Date();


                    } else {
                        //On prend la prevision pour l'heure i
                        hour = data.forecast.forecastday[jour].hour[i]

                        //Et l'heure de l'heure i
                        var date = new Date(hour.time_epoch * 1000);
                    }



                    //Arrangement des données
                    temp = hour.feelslike_c

                    //Récupération de l'heure
                    time = date.getHours() + ":00"

                    //Image correspondante à la météo
                    imgLink = hour.condition.icon

                    //Ajout de la carte correspondante
                    addWeatherCard(temp, time, imgLink)
                }
            }
        })
}

function addWeatherCard(temp, time, imgLink, firstOne = false) {
    //Récupération de la liste de carte
    const cardList = document.getElementById("weatherCardList")

    nbCardsShown += 1 //Ajout de 1 à la variable comptant le nombre de carte

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
    cardList.innerHTML += '\
        <li class="list-group-item col-1" style="border: none;background:none; ">\
            <div class="card text-center" style="">\
                <div class="card-header">\
                    <span class="' + tempClass + ' fs-5">' + temp + '</span>\
                </div>\
                <div class="card-body">\
                    <img src="https:' + imgLink + '" style="width: 8vh; height:auto">\
                </div>\
                <div class="card-footer text-muted fs-6">\
                    ' + time + '\
                </div>\
            </div>\
        </li>\
    '
}

//Première éxécution de la fonction quand la page a chargé
getWeatherInfos()

//Execution de la fonction toutes les 55s 
setInterval(() => {
    let date = new Date()
    //Si la minute actuelle est 0 ou 30, on réactualise les données de l'écran 
    if (date.getMinutes() == "0" || date.getMinutes() == "30") {
        getWeatherInfos()
    }
}, 55000)
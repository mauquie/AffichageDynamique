function getWeatherInfos() {
    //Récupération des informations de l'api pour la météo
    fetch("http://api.weatherapi.com/v1/current.json?key=30349e9636cc4e749c5203053210310&q=Montauban&aqi=no", {
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
            //Récupération de la température
            temp = data.current.temp_c

            //Image correspondante à la météo
            imgLink = data.current.condition.icon

            //Ajout des données au widget
            changeWidget(temp, imgLink)


        })
}

function changeWidget(temp, imgLink) {
    //Ajout d'un style à la température quand il fait trop froid ou trop chaud
    var domImage = document.getElementById("weatherImage")
    var domTemp = document.getElementById("weatherTemp")

    if (temp <= 10) {
        tempClass = "tempCold"

    } else if (temp >= 28) {
        tempClass = "tempHot"

    } else {
        tempClass = ""
    }

    var tempText = temp + "°C"


    domTemp.classList += " " + tempClass
    domTemp.innerText = tempText

    domImage.src = imgLink
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
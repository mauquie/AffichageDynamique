//Récupération des elemens DOM
DOMRepasType = document.getElementById("repasType")
DOMListAliment = document.getElementById("listAliment")
DOMMessageRepasVide = document.getElementById("messageRepasVide")

function getMenus() {
    //Variable utilisé pour récupérer la date d'aujourd'hui + l'heure actuelle
    dateTime = new Date()

    //Formatage de la date pour la requete vers le serveur (AAAA-MM-JJ)
    date = dateTime.getFullYear() + "-" + (dateTime.getMonth() + 1) + "-" + dateTime.getDate()

    //Requete vers le serveur
    fetch("/api/menus?date=2021-10-22" ).then((response) => {
        return response.json()

    }).then((data) => {
        //S'il n'y a pas de repas à afficher
        if (data.length == 0) {
            toggleMenu(true)

        } else { //S'il y a au moins un repas à afficher
            //On affiche le menu
            toggleMenu(false)

            //On récupère l'heure actuelle
            hour = dateTime.getHours()

            //S'il est - 15:00 ou qu'il n'y a qu'un seul repas pour aujourd'hui on affiche le repas de midi
            if (hour < 15) {
                repas = data[0]

            } else { //Sinon on affiche le repas du soir
                if (data.length > 1){
                    repas = data[1]

                } else {
                    toggleMenu(true)
                    return null
                }

            }

            // Pour chaque partie du repas, on assemble la liste d'aliment avec des "/" et on 
            // les affiche dans la liste des aliments sur la page
            for (let i = 0; i < Object.keys(repas.repas).length; i++) {
                partieDuRepas = repas.repas[i + 1]

                DOMListAliment.children[i].innerText = repas.repas[i + 1].join(" / ")
            }
        }
    })
}

function toggleMenu(toHide) {
    /*
        Affiche ou cache le menu en fonction du parametre toHide
    */
    if (toHide) {
        //On cache le menu et on affiche le message
        DOMMessageRepasVide.hidden = false
        DOMListAliment.hidden = true

    } else {
        //On affiche le menu et on cache le message
        DOMMessageRepasVide.hidden = true
        DOMListAliment.hidden = false

    }

    setCorrectMenu()

}

function setCorrectMenu() {
    /*
        Affiche le bon texte de presentation du menu, avec l'heure il choisi d'afficher soit "Midi" soit "Soir"
    */
    hour = dateTime.getHours()
    if (hour < 15) {
        DOMRepasType.innerText = "Pour ce midi,"

    } else {
        DOMRepasType.innerText = "Pour ce soir,"
    }
}

//Interval de 1mn (1000ms * 60)
setInterval(() => {
    getMenus()
}, 1000 * 60 * 1)

getMenus()
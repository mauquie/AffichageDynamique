function getMenus() {
    //Variable utilisé pour récupérer la date d'aujourd'hui + l'heure actuelle
    dateTime = new Date()

    //Formatage de la date pour la requete vers le serveur (AAAA-MM-JJ)
    date = dateTime.getFullYear() + "-" + (dateTime.getMonth() + 1) + "-" + dateTime.getDate()

    // Récupération de la clé unique de l'écran
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);

    //Requete vers le serveur
    fetch("/api/meals?date=" + date + "&k=" + urlParams.get('k')).then((response) => {
        return response.json()

    }).then((data) => {
        if (data.length < 1){
            toggleMenu(true, true)
            toggleMenu(true, false)
        } else {
            for (let i = 0; i < data.length; i++){
                toggleMenu(false, data[i].is_midday)
                setMenu(data[i].is_midday, data[i].meal)

            }
        }
    })
}

function toggleMenu(toHide, isMidi=true) {
    /*
        Affiche ou cache le menu en fonction du parametre toHide
    */
    let menuDOM = (isMidi) ? document.getElementById("midiList") : document.getElementById("soirList")

    if (toHide) {
        //On cache le menu et on affiche le message
        menuDOM.children[1].hidden = true
        menuDOM.children[0].hidden = false
        

    } else {
        //On affiche le menu et on cache le message
        menuDOM.children[1].hidden = false
        menuDOM.children[0].hidden = true

    }

}

function setMenu(isMidi, repas){
    let menuDOM = (isMidi) ? document.getElementById("midiList") : document.getElementById("soirList")

    let ulDOM = menuDOM.children[1]
        
    ulDOM.innerHTML = ""
    ulDOM.classList = "list"
        
    for(let i = 1; i < 7; i++){
        let partieDuRepas = repas[i].join(" / ")

        let itemListDOM = document.createElement("li")

        itemListDOM.innerText = partieDuRepas
        itemListDOM.classList = "list-item"

        ulDOM.appendChild(itemListDOM)
    }

    menuDOM.appendChild(ulDOM)
}

//Interval de 1mn (1000ms * 60)
setInterval(() => {
    getMenus()
}, 1000 * 60 * 1)

getMenus()
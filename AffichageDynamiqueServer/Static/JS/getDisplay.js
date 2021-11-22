//Récupération du paramètre GET de la page
const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);

//Récupération des informations sur la page actuelle
const code_name = urlParams.get("name")
const page_description = document.title

function getDisplay() {
    //Récupération des informations sur l'écran actuel
    fetch('/api/displays?code_name=' + code_name)
        .then((response) => {
            return response.json()
        })
        .then((data) => {
            //Si la description de la page à afficher n'est pas la même que celle affichée
            if (data[0].page != page_description){
                //On recharge la page
                location.reload()
            }

        })
}

setInterval(()=>{getDisplay()}, 5000)
domTitreEvenement = document.getElementById("titreEvenement")
domContenuEvenement = document.getElementById("contenuEvenement")
domCarteEvenement = document.getElementById("carteEvenement")
indexEvenement = 0
intervalEvenements = null
ancientEventTitre = null
ancientEventDescription = null


function animeEntreeEvenement()
{
    anime({
        targets: domCarteEvenement,
        translateX: 0, 
        easing: 'cubicBezier(0.110, 0.015, 0.700, 0.115)',
    })
}

function animeSortieEvenement()
{
    animationArticle = anime({ 
        targets: domCarteEvenement,
        translateX: 500, 
        easing: 'cubicBezier(0.000, 0.175, 0.080, 0.770)',
    })
    return animationArticle
}
//fonction gérant l'affichage et le bon bouclage des évènements
function affichageBouclage(events)
{   //incrémentation de l'index et vérifications qu'il ne soit pas trop grand
    indexEvenement++
    if (indexEvenement > events.length-1)
    {
        indexEvenement = 0
    }
    //on modifie l'affichage que si l'événement à afficher est différent de l'événement affiché.
    if (ancientEventTitre != events[indexEvenement].summary || ancientEventDescription != events[indexEvenement].description)
    { 
        animeSortieEvenement().finished.then(()=>
        {
            affichageEvents(events[indexEvenement]) //affichage, tour à tour, des évènements
            animeEntreeEvenement()
        })
    }

}

function getCalendar() 
{
    intervalEvenements = "lol"
    //Id du calendrier, trouvable dans les paramètres de google agenda.
    var calendarId = 'mbetous82@gmail.com'
    //Clef d'API, mise en place sur Console Google Cloud
    var apiKey = 'AIzaSyDHxOb1TYZJE288SIVD6UVR-ghAczOXAAs'
    var userTimeZone = "Europe/Paris"

    gapi.client.init({
        'apiKey': apiKey,
        //Doc du calendriers, nécessaire pour le fonctionnement.
        'discoveryDocs': ['https://www.googleapis.com/discovery/v1/apis/calendar/v3/rest'],
    }).then(() => {
        dateMax = new Date()
        dateMax.setDate(dateMax.getDate()+2) //on ne veut pas récupérer des événements qui auront lieu
        dateMax.setHours(23, 59, 59)  //dans plus de 2 jours
        return gapi.client.calendar.events.list({
            'calendarId': calendarId, 
            'timeZone': userTimeZone,
            'singleEvents': true, //Permet d'obtenir les évènements récurrents en tant qu'évènements uniques.
            'timeMin': (new Date()).toISOString(), //Évite de donner les évènements passés.
            'timeMax': dateMax.toISOString(),
            'orderBy': 'startTime'
        })
    }).then(response => {
        events = response.result.items //récupération des items, c'est à dire des événements.
        if (events.length == 0)
        {
            domCarteEvenement.hidden = true  //on cache l'event s'il n'y en a pas
            return
        }
        else
        {
            domCarteEvenement.hidden = false
            affichageBouclage(events) //on l'appelle avant le setInterval pour que l'évènement s'affiche instantanément
            intervalEvenements = setInterval(()=> //recupération de l'interval pour le clear à chaque refresh
            {      
                affichageBouclage(events)
            }, 20000)
            
        }
    })
}

function affichageEvents(event) 
{
    if (event.summary == undefined)
    {
        ancientEventTitre = event.summary //conservation du titre, pour vérifications dans Bouclage()
        domTitreEvenement.innerHTML = "Évènement : "
    }
    else //si le titre n'était pas précisé, on met un titre par défaut
    {
        ancientEventTitre = event.summary
        domTitreEvenement.innerHTML = event.summary
    }
    if (event.description == undefined)
    {
        ancientEventDescription = event.description //conservation de la desc, pour vérifications dans Bouclage()
        domContenuEvenement.innerHTML = ""
    }
    else //si la description n'était pas précisée, on met une chaîne vide
    { 
        ancientEventDescription = event.description
        domContenuEvenement.innerHTML = event.description
    }
}
gapi.load('client', getCalendar) //load de l'api de google calendar
setInterval(() =>
{
    if (intervalEvenements)
    {
        clearInterval(intervalEvenements) //clear afin de ne pas accumuler des boucles
    }
    gapi.load('client', getCalendar())
    
}, 1000 * 60 * 15)

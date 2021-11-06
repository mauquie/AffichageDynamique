domTitreEvenement = document.getElementById("titreEvenement")
domContenuEvenement = document.getElementById("contenuEvenement")
domCarteEvenement = document.getElementById("carteEvenement")
indexEvenement = 0
intervalEvenements = null

function affichageBouclage(events)
{
    if (indexEvenement > events.length-1)
    {
        indexEvenement = 0
    }
    affichageEvents(events[indexEvenement]) //affichage, tour à tour, des évènements
    indexEvenement++
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
        dateMax.setDate(dateMax.getDate()+2) 
        dateMax.setHours(23, 59, 59)
        return gapi.client.calendar.events.list({
            'calendarId': calendarId, 
            'timeZone': userTimeZone,
            'singleEvents': true, //Permet d'obtenir les évènements récurrents en tant qu'évènements uniques.
            'timeMin': (new Date()).toISOString(), //Évite de donner les évènements passés.
            'timeMax': dateMax.toISOString(),
            'orderBy': 'startTime'
        })
    }).then(response => {
        events = response.result.items
        if (events.length == 0)
        {
            domCarteEvenement.hidden = true
            return
        }
        else
        {
            domCarteEvenement.hidden = false
            affichageBouclage(events) //on l'appelle avant le setInterval pour que l'évènement s'affiche instantanément
            intervalEvenements = setInterval(()=> //recupération de l'interval pour le clear à chaque refresh
            {                                     //du calendar (dans le setInterval à la fin)
                affichageBouclage(events)
            }, 15000)
            
        }
    })
}

function affichageEvents(event) 
{
    if (event.summary == undefined)
    {
        domTitreEvenement.innerHTML = "Évènement : "
    }
    else
    {
        domTitreEvenement.innerHTML = event.summary
    }
    if (event.description == undefined)
    {
        domContenuEvenement.innerHTML = ""
    }
    else
    {
        domContenuEvenement.innerHTML = event.description
    }
}
gapi.load('client', getCalendar)
setInterval(() =>
{
    if (intervalEvenements)
    {
        clearInterval(intervalEvenements) //clear afin de ne pas accumuler des boucles
    }
    gapi.load('client', getCalendar())
    
}, 1000 * 30 * 1)

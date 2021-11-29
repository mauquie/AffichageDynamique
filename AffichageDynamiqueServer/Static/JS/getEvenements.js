indexEvenement = 1
intervalEvenements = null
domEventId = "ev-"
domDateId = "date-"
domEv1 = document.getElementById("ev-0")
domEv2 = document.getElementById("ev-1")
domEv3 = document.getElementById("ev-2")
domDate1 = document.getElementById("date-0")
domDate2 = document.getElementById("date-1")
domDate3 = document.getElementById("date-2")

dictMois = {
    0 : "Jan",
    1 : "Fev",
    2 : "Mar",
    3 : "Avr",
    4 : "Mai",
    5 : "Juin",
    6 : "Juil",
    7 : "Août",
    8 : "Sep",
    9 : "Oct",
    10 : "Nov",
    11 : "Dec",
}

function nettoyage()
{
    //nettoyage des dom évènements
    domEv1.innerText = ""
    domEv2.innerText = ""
    domEv3.innerText = ""
    domDate1.innerText = ""
    domDate2.innerText = ""
    domDate3.innerText = ""
}

//fonction gérant l'affichage et le bon bouclage des évènements
function affichageBouclage(listeEvents, once)
{ 
    //si once=true, cela siginifie qu'il y a
    // 3 (ou moins) évènements. On ne les fera donc pas tourner.
    if (once)
    {
        nettoyage()
        for (i=0; i < listeEvents.length; i++)
        {
            domEvent = document.getElementById(domEventId + String(i))
            domDate = document.getElementById(domDateId + String(i))
            dateEvent = new Date(listeEvents[i].start.dateTime)
            domDate.innerText = dateEvent.getDate() + " " + dictMois[dateEvent.getMonth()] 
            domEvent.innerText = listeEvents[i].summary
        }
        indexEvenement = 1 //Reinitialise index des events pour la prochaine fois où il y aura > 3 events
    }
    else
    {
        if (indexEvenement+3 > listeEvents.length)
        {
            indexEvenement = 0
        }
        domEventListe = [//liste des doms à animer
            domEv1,
            domEv2,
            domEv3,
        ]
        domDateListe = [
            domDate1,
            domDate2,
            domDate3,
        ]
        indexDom = 0 //index pour récupérer les doms de l'event / la date.
        animeSortieEvent(domEventListe).finished.then(()=>
        { //on les cache puis :
            nettoyage()
            for(i=indexEvenement; i < indexEvenement+3; i++)
                { //on remplace les textes
                    domEventListe[indexDom].innerText = listeEvents[i].summary
                    domDateListe[indexDom].innerText = new Date(listeEvents[i].start.dateTime).getDate()
                    indexDom++//et on incrémente index DOM pour modifier au prochain tour l'évènement suivant
                }
            animeEntreeEvent(domEventListe)
            indexEvenement++
        })
    }
}    
//retourne la liste des évènements à afficher.
function prepareListeEvents(events)
{
    eventsAuj = []
    eventsTrois = []
    for (i=0; i < events.length; i++)
    {
        if (new Date(events[i].start.dateTime).getDate() == new Date().getDate())
        {
            eventsAuj.push(events[i])
        }
    }
    //Si aujourd'hui, il y a + de 3 events, on les fera tourner. On les récupère tous.
    if (eventsAuj.length > 3)
    {
        return eventsAuj
    }
    //Sinon on affichera seulement les 3 premiers chronologiquement, peu importe la date .
    else
    {
        i = 0
        while (i < 3 && i < events.length)
        {
            eventsTrois.push(events[i])
            i++
        }
        return eventsTrois
    }
}

function animeEntreeEvent(domEvent)
{
    anime({
        targets: domEvent,
        duration: 800,
        opacity: [0, 1],
        easing: "linear",
        delay: 400
    })
}

function animeSortieEvent(domEvent)
{
    animationArticle = anime({
        targets: domEvent,
        duration: 800,
        opacity: [1, 0],
        easing: "linear",
    })
    return animationArticle
}

function getCalendar() 
{
    intervalEvenements = null
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
        dateMax.setDate(dateMax.getDate()+5) //on ne veut pas récupérer des événements qui auront lieu
        dateMax.setHours(23, 59, 59)  //dans plus de 5 jours
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
            document.getElementById("agenda").hidden = true
        }
        else
        {
            document.getElementById("agenda").hidden = false
            listeEvents = prepareListeEvents(events)
            if (listeEvents.length < 4)
            {
                affichageBouclage(listeEvents, true)
                return
            }
            else
            {
                affichageBouclage(listeEvents, false)
                intervalEvenements = setInterval(()=> //recupération de l'interval pour le clear à chaque refresh
                {      
                    affichageBouclage(listeEvents, false)
                }, 1000 * 30)    
            }
        }
    })
}

gapi.load('client', getCalendar) //load de l'api de google calendar
setInterval(() =>
{
    if (intervalEvenements)
    {
        clearInterval(intervalEvenements) //clear afin de ne pas accumuler des boucles
    }
    gapi.load('client', getCalendar())
    
}, 1000 * 60 * 60)

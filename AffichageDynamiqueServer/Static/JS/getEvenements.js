indexEvenement = 0
intervalEvenements = null
domEventId = "ev-"
dom1 = document.getElementById("ev-0")
dom2 = document.getElementById("ev-1")
dom3 = document.getElementById("ev-2")


function nettoyage()
{
    //nettoyage des dom évènements
    dom1.innerText = ""
    dom2.innerText = ""
    dom3.innerText = ""
}

//fonction gérant l'affichage et le bon bouclage des évènements
function affichageBouclage(listeEvents, once)
{ 
    nettoyage()
    //si once, cela siginifie qu'il y a 3 ou moins évènements.
    //on ne les fera donc pas tourner.
    if (once)
    {
        for (i=0; i < listeEvents.length; i++)
        {
            domEvent = document.getElementById(domEventId + String(i))
            domEvent.innerText = listeEvents[i].summary
        }
    }
    else
    {
        if (indexEvenement+3 > listeEvents.length)
        {
            indexEvenement = 0
        }
        domEventList = [//liste des doms à animer
            dom1,
            dom2,
            dom3,
        ]
        indexDom = 0 //index pour récupérer la dom de l'event.
        animeSortieEvent(domEventList).finished.then(()=>{ //on les cache puis :
        for(i=indexEvenement; i < indexEvenement+3; i++)
            { //on remplace les textes
                domEventList[indexDom].innerText = listeEvents[i].summary
                indexDom++//et on incrémente index DOM pour modifier au prochain tour l'évènement suivant
            }
        indexEvenement++
        animeEntreeEvent(domEventList)
        })
    }
}    
//retourne la liste des évènements à afficher.
function prepareListe(events)
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
        console.log(eventsAuj)
        return eventsAuj
    }
    //Sinon on affichera seulement les 3 premiers chronologiquement.
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
            listeEvents = prepareListe(events)
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
                }, 6000)    
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
    
}, 1000 * 20)

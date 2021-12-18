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

//fonction qui affiche / cache les cases vides d'évènements
function displayEventsContainer(listeEvents)
{
    domDateContainer1 = document.getElementById("date-first")
    domDateContainer2 = document.getElementById("date-second")
    domDateContainer3 = document.getElementById("date-third")
    domEvContainer1 = document.getElementById("ev-first")
    domEvContainer2 = document.getElementById("ev-second")
    domEvContainer3 = document.getElementById("ev-third")
    domListeDate = document.getElementById("liste-date")
    domListeEv = document.getElementById("liste-evenement")
    listDateContainers = [domDateContainer1, domDateContainer2, domDateContainer3]
    listeEvContainers = [domEvContainer1, domEvContainer2, domEvContainer3]
    if (listeEvents.length > 0)
    {
        for (i=2; i >= listeEvents.length; i--)
        {
            listDateContainers[i].hidden = true
            listeEvContainers[i].hidden = true
        }
        for (i=listeEvents.length-1; i >= 0; i--)
        {
            listDateContainers[i].hidden = false
            listeEvContainers[i].hidden = false
        }
        domListeDate.style.transform = "translateX(" + 17*(3-listeEvents.length) + "vh) translateY(-27%)"
        domListeEv.style.transform = "translateX(" + 17*(3-listeEvents.length) + "vh) translateY(-2.3vh)"
    }


}

//fonction vérifiant que l'évènement ne dépasse pas le container, si oui : raccourcissement du texte
function checkHeight(domEv, raccourci)
{
    domContainerEv = document.getElementById("container-evenement")
    { //si le texte dépasse le container,
        if (domEv.clientHeight > domContainerEv.clientHeight)
        {
            text = domEv.innerText
            dernierEspace = text.lastIndexOf(" ") //on récupère l'index du dernier espace
            domEv.innerText = text.substring(0, dernierEspace) //et on ne garde que le texte jusqu'à cet espace (on supprime le dernier mot)
            checkHeight(domEv, true)//on vérifie si le texte rentre désormais.
        }
        else
        {   //s'il rentre et qu'il a été raccourci,
            if (raccourci)
            { //on ajoute "..." et on vérifie qu'après cet ajout le texte entre encore
                domEv.innerText += "..."
                if (domEv.clientHeight > domContainerEv.clientHeight)
                {//s'il ne rentre plus dans le container,
                    checkHeight(domEv, true) //on réappelle la fonction, qui reréduira et réajoutera les "...".
                }
            }
            //s'il n'a pas été raccourci et qu'il rentre, on ne touche à rien
        }
    }
}

function nettoyage()
{
    //vide les dom évènements
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
            checkHeight(domEvent, false)
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
                    checkHeight(domEventListe[indexDom], false)
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
        return gapi.client.calendar.events.list({
            'calendarId': calendarId, 
            'timeZone': userTimeZone,
            'singleEvents': true, //Permet d'obtenir les évènements récurrents en tant qu'évènements uniques.
            'timeMin': (new Date()).toISOString(), //Évite de donner les évènements passés.
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
                displayEventsContainer(listeEvents)
                affichageBouclage(listeEvents, true)
                return
            }
            else
            {
                displayEventsContainer(listeEvents)
                affichageBouclage(listeEvents, false)
                intervalEvenements = setInterval(()=> //recupération de l'interval pour le clear à chaque refresh
                {      
                    displayEventsContainer(listeEvents)
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

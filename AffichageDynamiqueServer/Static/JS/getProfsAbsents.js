indexProfs = 1
DOMtextePasAbsences = document.getElementById("textePasAbsences")
DOMlisteProfs = document.getElementById("listeProfs")
DOMlisteProfsContainer = document.getElementById("prof-list")
DOMlisteProfsCachable = document.getElementById("listeProfsCachable")
intervalScroll = null
direction = "down"


//prépare la liste des professeurs absents : formate les heures, trie en fonction des heures.
function prepareListeProfs(listeProfs)
{
    listeProfs = listeProfs.sort((a, b)=> {   //tri des profs absents en fonction de l'heure
        return new Date(a.fin).getHours() - new Date(b.fin).getHours() //de fin d'absence
        })
    listeProfs = listeProfs.sort((a, b)=> {   //puis tri des profs absents en fonction de l'heure
    return new Date(a.debut).getHours() - new Date(b.debut).getHours() //de début d'absence
    }) //afin d'obtenir une liste triée en facteur premier l'heure de début, et en facteur second l'heure de fin
    for (i = 0; i < listeProfs.length; i++)
    {
        heureDebut = listeProfs[i].debut.slice(0, listeProfs[i].debut.length - 1) //suppresion du "Z"
        heureDebut = (new Date(heureDebut).getHours())
        listeProfs[i].debut = heureDebut //changement du dateTime du début de prof, en uniquement l'heure

        heureFin = listeProfs[i].fin.slice(0, listeProfs[i].fin.length - 1)
        heureFin = (new Date(heureFin).getHours()) //idem pour le dateTime de la fin du prof.
        listeProfs[i].fin = heureFin
    }
    return listeProfs
}

//remplie les li de l'affichage par les profs.
function affichageProfs(listeProfs)
{
    DOMlisteProfsLI = document.getElementById("listeProfs").getElementsByTagName("li")
    while (DOMlisteProfsLI.length != 0)
    {
        DOMlisteProfsLI[0].remove()
    }

    for (i=0; i<listeProfs.length; i++)
    {
        listProfElemDOM = document.createElement("li")
        listProfElemDOM.innerText = listeProfs[i].debut + "h - " + listeProfs[i].fin + "h | " + listeProfs[i].prof
        listProfElemDOM.classList = "list-item liste-profs"
        DOMlisteProfs.appendChild(listProfElemDOM)
    }
}

function scrolling(len, occurencesNumber)
{  
    DOMlisteProfsContainer.scrollBy(0, len/Math.abs(len))
    occurencesNumber++
    if (occurencesNumber >= Math.abs(len))
    {
        return
    }
    delay = setTimeout(() => {
        scrolling(len, occurencesNumber)
    }, 10)
}

//a pour rôle de gérer le scrolling, pour afficher tous les profs
function scrollingHandler(listeProfs) 
{//Le scrolling se fait une longueur de liste par une longueur de liste
    if (listeProfs.length > 5) //Si la liste est > que 5 profs, il faut scroll
    {
        if (direction=="down") //Si on descendait au tour précédant,
        {
            if (DOMlisteProfsContainer.scrollTop*1.3 > DOMlisteProfsContainer.scrollHeight-DOMlisteProfsContainer.clientHeight) //Et si on est presque arrivé en bas du scrolling,
            {
                scrolling(DOMlisteProfsContainer.clientHeight*((listeProfs.length%5)/5), 0)//alors on descend de juste ce qu'il faut,
                direction = "up" //et on change la direction
            }
            else //Sinon, c'est qu'il faut encore descendre, donc
            {
                scrolling(DOMlisteProfsContainer.clientHeight+window.innerHeight/330, 0)//on descend 
            }
        }
        else if (direction == "up")
        {
            if (DOMlisteProfsContainer.scrollTop == 0)//Si on est remonté tout en haut donc
            {
                scrolling(DOMlisteProfsContainer.clientHeight+window.innerHeight/330, 0)//on descend,
                direction = "down" //on change la direction
            }
            else
            {//sinon il faut continuer à remonter alors
                scrolling(-DOMlisteProfsContainer.clientHeight-window.innerHeight/330, 0)//on monte
            }
        }//les + et - windowHeight sont des ajustements nécessaires, plus l'écran est grand,
        //plus il y avait un décalage dans le scrolling.
    }
}

function getProfsAbs()
{
    fetch("/api/profsAbs").then(response => {
        return response.json()
    }).then(data => {
        if (data.length == 0)
        {
            DOMtextePasAbsences.hidden = false
            DOMlisteProfsCachable.hidden = true
            return
        }
        else if (data.length > 5)
        {
            DOMtextePasAbsences.hidden = true
            DOMlisteProfsCachable.hidden = false
            listeProfs = prepareListeProfs(data) //préparation pour afficher la liste (tri + changer heures)
            affichageProfs(listeProfs)
            if (intervalScroll)
            {
                clearInterval(intervalScroll)
            }
            intervalScroll = setInterval(() =>
            {
                scrollingHandler(listeProfs)
            }, 7000)
        }
        else
        {
            DOMtextePasAbsences.hidden = true
            DOMlisteProfsCachable.hidden = false
            listeProfs = prepareListeProfs(data) //préparation pour afficher la liste (tri + changer heures)
            affichageProfs(listeProfs)
        }
    })
}
interval = getProfsAbs()
setInterval(() => 
{
    if(interval)
    {
        clearInterval(interval) //clear afin de ne pas accumuler des boucles
    }
    interval = getProfsAbs()
}, 1000 * 60 * 60)

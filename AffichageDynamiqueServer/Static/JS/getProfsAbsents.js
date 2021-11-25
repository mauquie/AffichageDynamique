indexProfs = 0
DOMtextePasAbsences = document.getElementById("textePasAbsences")
DOMlisteProfs = document.getElementById("listeProfs").getElementsByTagName("li")
DOMlisteProfsCachable = document.getElementById("listeProfsCachable")


//divise la liste des profs en une liste de groupes de 5 profs.
function divideProfs(listeProfs)
{
    listeGroupesProfs = [] //on affiche seulement 5 profs à la fois.
    for (i = 0; i < (listeProfs.length / 5); i++) //donc création de i sous listes de 5 profs
    {
        listeTemp = []
        for (j = 0; j < 5 && j+(5*i) < listeProfs.length; j++) //ajoute des profs tant qu'il en reste,                                      
        {                                            //et tant que la sous liste contient - de 5 profs.
            listeTemp.push(listeProfs[j+(5*i)]) 
        }
        listeGroupesProfs.push(listeTemp) //ajout de la sous liste dans une liste mère
    }
    return listeGroupesProfs
}

//prépare la liste des professeurs absents : formate les heures, trie en fonction des heures.
function prepareListe(listeProfs)
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
        heureDebut = new Date(heureDebut).getHours() 
        listeProfs[i].debut = heureDebut //changement du dateTime du début de prof, en uniquement l'heure

        heureFin = listeProfs[i].fin.slice(0, listeProfs[i].fin.length - 1)
        heureFin = new Date(heureFin).getHours() //idem pour le dateTime de la fin du prof.
        listeProfs[i].fin = heureFin
    }
    return listeProfs
}

//remplie les li de l'affichage par les profs.
function affichageProfs(listeProfs)
{
    for (i=0; i < 5; i++)
    {
        DOMlisteProfs[i].innerHTML = ""
    }
    //remplie les li
    for (i=0; i < listeProfs.length; i++)
    {
        DOMlisteProfs[i].style.visibility = "visible"
        DOMlisteProfs[i].innerHTML = listeProfs[i].debut + "h - " + listeProfs[i].fin + "h | " + listeProfs[i].prof 
    }
    //cache les li vides
    for (i=0; i < 5; i++)
    {
        if (DOMlisteProfs[i].innerHTML == "")
        {
            DOMlisteProfs[i].style.visibility="hidden"
        }
    }
    
}

function animeEntreeProfs()
{
    animationArticle = anime({
        targets: DOMlisteProfs,
        duration: 800,
        opacity: [0, 1],
        easing: "linear",
        delay: 400,
    })
}

function animeSortieProfs()
{
    animation = anime({
        targets: DOMlisteProfs,
        duration: 800,
        opacity: [1, 0],
        easing: "linear"
    })
    return animation
}

function bouclage() //a pour rôle de gérer la boucle, pour afficher les profs
{
    if (indexProfs > listeGroupesProfs.length-1)
    {
        indexProfs = 0
    }
        affichageProfs(listeGroupesProfs[indexProfs])
        //affichage, tour à tour, des sous listes
        indexProfs++
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
        else
        {
            DOMtextePasAbsences.hidden = true
            DOMlisteProfsCachable.hidden = false
            listeProfs = prepareListe(data) //préparation pour afficher la liste (tri + changer heures)
            listeGroupesProfs = divideProfs(listeProfs) //division de la liste en sous liste de taille 5
            animeSortieProfs().finished.then(() => {
                bouclage() //bouclage avant l'interval, pour afficher immédiatement les profs absents.
                animeEntreeProfs()
            }) 
            if (listeGroupesProfs.length > 1)
            {
                interval = setInterval(()=>
                {
                    animeSortieProfs().finished.then(() => {
                        bouclage()
                        animeEntreeProfs()
                    })
                }, 1000 * 20)
                return interval
            }
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

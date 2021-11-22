indexProfs = 0
DOMtextePasAbsences = document.getElementById("textePasAbsences")
DOMlisteProfs = document.getElementById("listeProfs").getElementsByTagName("li")
DOMlisteProfsCachable = document.getElementById("listeProfsCachable")

alert(DOMlisteProfs[0].innerHTML)
/*
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
    return new Date(a.debut).getHours() - new Date(b.debut).getHours() //de début d'absence
    })
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
    DOMlisteProfs.innerText = ""
    for (i = 0; i < listeProfs.length; i++)
    {
        row = DOMlisteProfs.insertRow(-1)
        cell1 = row.insertCell(0)
        cell2 = row.insertCell(1)
        cell1.innerText = listeProfs[i].prof 
        cell2.innerText = listeProfs[i].debut + "h - " + listeProfs[i].fin + "h"
        cell1.style.textAlign = "center"
        cell2.style.textAlign = "center" 
    }
}

function animeEntree()
{
    anime({ //anime haut-bas-droite
        targets: DOMlisteProfsCachable,
        translateX: 0, 
        easing: 'cubicBezier(0.110, 0.015, 1.000, 0.115)',
    })
}

function animeSortie()
{
    animation = anime({ //anime haut-bas-droite
        targets: DOMlisteProfsCachable,
        translateX: 800, 
        easing: 'cubicBezier(0.000, 0.275, 0.080, 0.970)',
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
            bouclage() //bouclage avant l'interval, pour afficher immédiatement les profs absents.
            if (listeGroupesProfs.length > 1)
            {
                interval = setInterval(()=>
                {
                    bouclage() //changements des profs
                }, 20000)
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
}, 1000 * 30 * 1)
*/
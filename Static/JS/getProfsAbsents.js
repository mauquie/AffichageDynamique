indexProfs = 0
DOMtextePasAbsences = document.getElementById("textePasAbsences")
DOMtableProfs = document.getElementById("tableProfs")
function divideProfs(listeProfs)
{
    listeGroupesProfs = [] //on affiche seulement 8 profs à la fois.
    for (i = 0; i < (listeProfs.length / 8); i++) //création de i sous listes de 8 profs
    {
        listeTemp = []
        for (j = 0; j < 8 && j+(8*i) < listeProfs.length; j++) //ajoute des profs tant qu'il en reste,                                      
        {                                            //et que la sous liste contient - de 8 profs.
            listeTemp.push(listeProfs[j+(8*i)]) 
        }
        listeGroupesProfs.push(listeTemp) //ajout de la sous liste dans une liste mère
    }
    return listeGroupesProfs
}

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

function affichageProfs(listeGroupesProfs)
{
    table = document.getElementById("table")
    table.innerText = ""
    for (i = 0; i < listeGroupesProfs.length; i++)
    {
        row = table.insertRow(-1)
        cell1 = row.insertCell(0)
        cell2 = row.insertCell(1)
        cell1.innerText = listeGroupesProfs[i].prof 
        cell2.innerText = listeGroupesProfs[i].debut + "h - " + listeGroupesProfs[i].fin + "h"
        cell1.style.textAlign = "center"
        cell2.style.textAlign = "center" 
    }
}

function bouclage() //a pour rôle de gérer la boucle, pour afficher les profs
{
    if (indexProfs > listeGroupesProfs.length-1)
    {
        indexProfs = 0
    }
    affichageProfs(listeGroupesProfs[indexProfs]) //affichage, tour à tour, des sous listes
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
            DOMtableProfs.hidden = true
            return
        }
        else
        {
            DOMtextePasAbsences.hidden = true
            DOMtableProfs.hidden = false
            listeProfs = prepareListe(data) //préparation pour afficher la liste (tri + changer heures)
            listeGroupesProfs = divideProfs(listeProfs) //division de la liste en sous liste de taille 8
            bouclage() //on l'appelle avant le setInterval pour que les absences s'affichent instantanément
            interval = setInterval(()=>
            {
                bouclage()
            }, 15000)
            return interval
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
}, 1000 * 60 * 5)
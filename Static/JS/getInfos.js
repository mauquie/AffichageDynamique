index=0

function getInformations() 
{
    fetch("/api/infos").then(response => {
        return response.json();

    }).then(data => {
        actualInfo = document.getElementById("infoContainer").innerText
        domInfoCachable = document.getElementById("containerCachable")
        if (index >= data.length) //bouclage de index
        {
            index = 0
        }
        if (data.length == 0) //on cache s'il n'y a rien à afficher
        {
            exitScreen().finished.then(() => {
                domInfoCachable.hidden = true
            })
        }
        else if (actualInfo != data[index].message) //vérification de la différence entre l'info actuelle et celle
        {                                           //à afficher, car aucune modifs à faire si ce sont les mêmes
            exitScreen().finished.then(() => //on fait sortir la div de l'écran, puis quand l'anim est finie :
            {
                changeInfo(data) //changement de l'info
                setSize() //adaptation de la taille du texte
                changeStyleInfo(data[index]) //changement du background
                enterScreen() //animation de l'entrée de la div
            })
        }
    });
    index++
}

function changeInfo(listeInfo)
{
    domInfo = document.getElementById("information")
    domInfoCachable = document.getElementById("containerCachable")

    domInfoCachable.hidden = false
    domInfo.innerHTML = listeInfo[index].message; 
    domInfo.style.fontSize="80px" //Taille de base de l'info, adaptée après par setSize().
}

function setSize()
{
    domContainerInfo = document.getElementById("infoContainer")
    pInfoDom = document.getElementById("information")
    if (pInfoDom.clientHeight > domContainerInfo.clientHeight)
    {
        fontSize = window.getComputedStyle(pInfoDom).fontSize //nécessaire pour transformer 
        fontSize = Number(fontSize.slice(0, fontSize.length-2))//"taille px" en une taille en int
        pInfoDom.style.fontSize = parseFloat(fontSize-1) + "px"//puis repasser en "taille px"
        setSize()
    }
}

function changeStyleInfo(info)
{ 

    domInfoContainer = document.getElementById("infoContainer")
    switch(info.type.id) {
        case 1:
            if (domInfoContainer.classList.contains("bg-secondary")) //remplacement du bg gris par
            {                                                        //le rouge
                domInfoContainer.classList.remove("bg-secondary")
            }
            domInfoContainer.classList.add("bg-danger")
            break;
        case 2:
            if (domInfoContainer.classList.contains("bg-danger"))//remplacement du bg rouge par                                                     
            {                                                   //le gris
                domInfoContainer.classList.remove("bg-danger")
            }
            domInfoContainer.classList.add("bg-secondary")
            break;
        default:
           break;
      }
}

function enterScreen()
{
    domInfoContainer = document.getElementById("infoContainer")
    anime({
        targets: domInfoContainer, //anime gauche-droite
        translateY: 0,
        easing: 'spring(1, 80, 10, 0)',
    })

    /*
    anime({ //anime haut-bas-droite
        targets: domInfoContainer,
        translateX: 0, 
        easing: 'spring(1, 80, 10, 0)',
    })
    */
}

function exitScreen()
{
    /*
    domInfoContainer = document.getElementById("infoContainer")
    tl = anime.timeline({ //anime gauche-droite
        targets: domInfoContainer
    })
    tl.add({
        easing: 'easeInElastic(1, 2)',
        translateX: domInfoContainer.clientWidth*2,
    })
    tl.add({
        translateX: -domInfoContainer.clientWidth*2,
        easing: 'steps(1)',
    })
    return tl
    */
    domInfoContainer = document.getElementById("infoContainer")
    tl = anime.timeline({ //haut-bas-droite
        targets: domInfoContainer
    })
    tl.add({
        easing: 'easeInElastic(1, 2)',
        translateX: domInfoContainer.clientWidth*2,
    })
    tl.add({
        translateY: -domInfoContainer.clientHeight*2,
        translateX: 0,
        easing: 'steps(1)',
    })
    return tl //return pour savoir dans getInformations quand l'animation est terminée
    
}
 
getInformations()
setInterval(() => {
    getInformations()
}, 20000)

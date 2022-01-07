indexInformations=0
domInfoContainer = document.getElementById("infoContainer")
domInfo = document.getElementById("information")

function getInformations() 
{
    fetch("/api/infos").then(response => {
        return response.json();

    }).then(data => {
        actuelleInfo = domInfo.innerHTML
        if (indexInformations >= data.length) //bouclage de indexInformations
        {
            indexInformations = 0
        }
        if (data.length == 0) //on cache s'il n'y a rien à afficher
        {
            animeSortieInfo().finished.then(() => {
                domInfoContainer.hidden = true
            })
        }
        else 
        {
            if (domInfoContainer.hidden)
            {
                domInfoContainer.hidden = false
                //anime.set(domInfoContainer, {
                //translateX: -domInfoContainer.clientWidth * 2
                //})
                changeInfo(data)
                setSize()
                //changeStyleInfo(data[indexInformations])
                //setTimeout(() =>{
                animeEntreeInfo()
                //}, 1000)
            }
            else if (actuelleInfo != data[indexInformations].message) //vérification de la différence entre l'info actuelle et celle
            {                                           //à afficher, car aucune modif à faire si ce sont les mêmes
                animeSortieInfo().finished.then(() => //on fait sortir la div de l'écran, puis quand l'anim est finie :
                {
                    changeInfo(data) //changement de l'info
                    setSize() //adaptation de la taille du texte
                    //changeStyleInfo(data[indexInformations]) //changement du background
                    animeEntreeInfo() //animation de l'entrée de la div
                })
            }
        }
    });
    indexInformations++
}

function changeInfo(listeInfo)
{
    domInfo.innerHTML = listeInfo[indexInformations].message; 
    domInfo.style.fontSize="4vh" //Taille de base de l'info, adaptée après par setSize().
    if (listeInfo[indexInformations].type.id == 1){
        domInfo.style.color = "#dc3545"
        domInfo.style.textShadow = "1px 1px 4px rgba(0, 0, 0, 0.3)"
    } else {
        domInfo.style.color = "#212529"
        domInfo.style.textShadow = ""
    }
}

function setSize()
{
    domContainerInfo = document.getElementById("infoContainer")
    pInfoDom = document.getElementById("information")
    if (pInfoDom.clientHeight > domContainerInfo.clientHeight)
    {
        fontSize = window.getComputedStyle(pInfoDom).fontSize //nécessaire pour transformer 
        fontSize = Number(fontSize.slice(0, fontSize.length-2))//"taille px" en une taille en int
        fontSizeVH = (fontSize/window.innerHeight)*100 //puis en taille vh
        pInfoDom.style.fontSize = parseFloat(fontSizeVH-0.1) + "vh"//puis repasser en "taille px"
        setSize()
    }
}

function changeStyleInfo(info)
{ 

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

function animeEntreeInfo() {
    anime({
        targets: domInfo,
        duration: 800,
        opacity: [0, 1],
        easing: "linear",
        delay: 400
    })
}

function animeSortieInfo() {
    animationArticle = anime({
        targets: domInfo,
        duration: 800,
        opacity: [1, 0],
        easing: "linear"
    })
    return animationArticle
}

 
getInformations()
setInterval(() => {
    getInformations()
}, 1000 * 15)

index=0
function changeInfo(listeInfo)
{
    var domInfo = document.getElementById("information")
    if (listeInfo.length == 0)
    {
        var domInfoCachable = document.getElementById("container-cachable")
        domInfoCachable.hidden = true
    }
    else
    {
        domInfo.hidden = false
        if (index >= listeInfo.length)
        {
            index = 0
        }
        var information = listeInfo[index].message;
        domInfo.innerHTML = information
        domInfo.style.fontSize="80px" //Taille de base de l'info, adaptée après par setSize().
        changeStyleInfo(listeInfo[index])
        index++
    }
}

function getInformations() 
{
    fetch("/api/infos").then(response => {
        return response.json();

    }).then(data => {
        changeInfo(data)
        setSize()
        playAnimation()
    });
}

function playAnimation()
/*{
    var domInfoContainer = document.getElementById("infoContainer")
    var tl = anime.timeline({
        targets: domInfoContainer
    })
    tl.add(
    {
        translateY: [-domInfoContainer.clientHeight*2,0],
        easing: 'spring(1, 80, 10, 0)',
    })
    tl.add(
    {
        delay: 13000,
        easing: 'easeInElastic(1, 2)',
        translateX: domInfoContainer.clientWidth*2,
    })
    tl.add({
        translateX: 0,
        translateY: -domInfoContainer.clientHeight*2,
        easing: 'steps(1)',
    }
    )

}
*/
/*
{
    var domInfoContainer = document.getElementById("infoContainer")
    var tl = anime.timeline({
        targets: domInfoContainer
    })
    tl.add(
    {
        translateX: [-domInfoContainer.clientWidth*2,0],
        easing: 'spring(1, 80, 10, 0)',
    })
    .add(
    {
        delay: 13000,
        easing: 'easeInElastic(1, 2)',
        translateX: domInfoContainer.clientWidth*2,
    })
    .add({
        translateX: -domInfoContainer.clientWidth*2,
        easing: 'steps(1)',
    })
}*/
{
    var domInfoContainer = document.getElementById("infoContainer")
    var tl = anime.timeline({
        targets: domInfoContainer
    })
    tl.add(
    {
        translateX: [-domInfoContainer.clientWidth*2,0],
        easing: 'spring(1, 80, 10, 0)',
    })
    .add(
    {
        delay: 16000,
        easing: 'easeInElastic(1, 2)',
        translateX: domInfoContainer.clientWidth*2,
    })
    .add({
        translateX: -domInfoContainer.clientWidth*2,
        easing: 'steps(1)',
    })
}

function setSize()
{
    domContainerInfo = document.getElementById("infoContainer")
    pInfoDom = document.getElementById("information")
    if (pInfoDom.clientHeight > domContainerInfo.clientHeight)
    {
        fontSize = window.getComputedStyle(pInfoDom).fontSize //nécessaire pour transformer 
        fontSize = Number(fontSize.slice(0, fontSize.length-2))//"taille en px" en taille int
        pInfoDom.style.fontSize = parseFloat(fontSize-2) + "px"//puis repasser en "taille en px"
        setSize()
    }
}

 
function changeStyleInfo(info)
{ 
    var domInfoContainer = document.getElementById("infoContainer")
    console.log(info.type.id)
    switch(info.type.id) {
        case 1:
            domInfoContainer.classList.add("bg-info")
            break;
        case 2:
            domInfoContainer.style.backgroundColor = "blue"
            break;
        default:
           break;
      }
}

/*anime.set({ //nécessaire, il faut que l'info initiallement au dessus de l'écran.
    targets: document.getElementById("infoContainer"),
    translateX: -(document.getElementById("infoContainer").clientWidth*2),
})
*/ 
getInformations()
setInterval(() => {
    getInformations()
}, 19000)

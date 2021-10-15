var text = document.getElementById("information") //Création d'un span pour mesurer la longeur du
var documentMesure = document.createElement("span") //texte d'information.
document.body.append(documentMesure)
documentMesure.style.cssText = text.style.cssText
documentMesure.style.position = "absolute"
documentMesure.style.top = "-200px"


index=0
function changeInfo(listeInfo)
{
    var domInfo = document.getElementById("information")
    if (listeInfo.length == 0)
    {
        domInfo.hidden = true
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
        domInfo.style.fontSize="80px"
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
    });
}

function playAnimation()
{
    var textInfo = document.getElementById("information")
    documentMesure.innerHTML = text.innerHTML
    textLength = documentMesure.offsetWidth
    anime({
        targets: textInfo,
        translateX: [-textLength, window.innerWidth],
        duration: (textLength+window.innerWidth)*10,
        easing: "linear",
        direction: "reverse",
    })
}

function setSize()
{
    domContainerInfo = document.getElementById("infoContainer")
    pInfoDom = document.getElementById("information")
    if (pInfoDom.clientHeight > domContainerInfo.clientHeight)
    {
        fontSize = window.getComputedStyle(pInfoDom).fontSize
        fontSize = Number(fontSize.slice(0, fontSize.length-2))
        pInfoDom.style.fontSize = parseFloat(fontSize-2) + "px"
        setSize()
    }
}

getInformations()
setInterval(() => {
    getInformations()
}, 5000)

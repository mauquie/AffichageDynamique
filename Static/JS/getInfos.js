var text = document.getElementById("information") //Création d'un span pour mesurer la longeur du
var documentMesure = document.createElement("span") //texte d'information.
document.body.append(documentMesure)
documentMesure.style.cssText = text.style.cssText
documentMesure.style.position = "absolute"
documentMesure.style.top = "-200px"


index=0
function changeInfo(listeInfo)
{
    var domInfo = document.getElementById("infoContainer")
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
        var information = "Information " + listeInfo[index].type.name + " : " + listeInfo[index].message;
        domInfo.innerHTML = information
        index++
    }
}

function getInformations() 
{
    fetch("/api/infos").then(response => {
        return response.json();

    }).then(data => {
        changeInfo(data)
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
    console.log("oui")
    domContainerInfo = document.getElementById("infoContainer")
    pInfoDom = document.getElementById("information")
    pInfoDom.fontSize+=1;
    if (domContainerInfo.clientHeight > pInfoDom.clientHeight)
    {
        console.log("vroum")
    }
    
}

getInformations()
setInterval(() => {
    getInformations()
}, 5000)

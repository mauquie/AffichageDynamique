var text = document.getElementById("information") //Création d'un span pour mesurer la longeur du
var documentMesure = document.createElement("span") //texte d'information.
document.body.append(documentMesure)
documentMesure.style.cssText = text.style.cssText
documentMesure.style.position = "absolute"
documentMesure.style.top = "-200px"

index=0
function getInformations() {
    fetch("/api/infos").then(response => {
        return response.json();

    }).then(data => {
        var domInfo = document.getElementById("information");
        if (data.length == 0)
        {
            domInfo.hidden = "true"
            return;
        }
        var domInfo = document.getElementById("information");
        var text = data[index].message
        var information = "Information " + data[index].type.name + " : " + data[index].message;
        domInfo.innerText = information;
        if (index==data.length-1)
        {
            index = -1
        }
        index++
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

function setSize(text)
{
    domContainerInfo = document.getElementById("infoContainer")
    
}

getInformations();
setInterval(() => {
    getInformations();
}, 50000)

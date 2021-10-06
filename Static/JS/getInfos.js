setInterval(() => {
        getInformations();
}, 5000),

getInformations();

index=0
function getInformations() {
    fetch("/api/infos").then(response => {
        return response.json();

    }).then(data => {
        var domInfo = document.getElementById("information");
        information = "Information " + data[index].type.name + " : " + data[index].message;
        domInfo.innerText = information;
        if (index==data.length-1)
        {
            index = -1
        }
        index++
    });
}
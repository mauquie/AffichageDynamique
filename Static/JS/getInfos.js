setInterval(() => {
        getInformations();
}, 5000),

getInformations();

function getInformations() {
    fetch("/api/infos").then(response => {
        return response.json();

    }).then(data => {
        var domInfo = document.getElementById("information");

        information = "Information " + data[0].type.name + " : " + data[0].message;
        domInfo.innerText = information;
    });
}
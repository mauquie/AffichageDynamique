DOMarticle = document.getElementById("article")
DOMPasArticle = document.getElementById("pasArticle")

days = {
    0 : "dimanche",
    1 : "lundi",
    2 : "mardi",
    3 : "mercredi",
    4 : "jeudi",
    5 : "vendredi",
    6 : "samedi",
}

months = {
    0 : "janvier",
    1 : "février",
    2 : "mars",
    3 : "avril",
    4 : "mai",
    5 : "juin",
    6 : "juillet",
    7 : "août",
    8 : "septembre",
    9 : "octobre",
    10 : "novembre",
    11 : "décembre",
}

//fade in de l'article
function animeEntreeArticle(domElement) {
    anime({
        targets: domElement,
        duration: 800,
        opacity: [0, 1],
        easing: "linear",
        delay: 400
    })
}

//fonction ajoutant la date du jour à l'article d'aujourd'hui
function setDefaultArticle()
{
    date = new Date()
    text = `Nous sommes le ${days[date.getDay()]} ${date.getDate()} ${months[date.getMonth()]} `
    text += "et la journée s'annonce plutôt "
    document.getElementById("text-no-article").innerText = text
}

//fade out de l'article
function animeSortieArticle(domElement) {
    animationArticle = anime({
        targets: domElement,
        duration: 800,
        opacity: [1, 0],
        easing: "linear"
    })
    return animationArticle
}

//fonction vérifiant que l'article ne dépasse pas sur l'agenda, si oui : rétrecissement du texte
function checkHeightArticle()
{
    //si l'article dépasse 53% de l'écran...
    DOMarticle = document.getElementById("article")
    if ((DOMarticle.clientHeight/window.innerHeight) > 0.53)
    {   
        domContenu = document.getElementById("contenuArticle")//on récupère le texte de l'article,
        fontSize = domContenu.style.fontSize
        fontSize = fontSize.substring(0, fontSize.length-2)
        fontSize -= 0.01
        domContenu.style.fontSize = fontSize + "vh"//on rétrécie le texte et
        checkHeightArticle()//on vérifie si le texte rentre désormais.
    }
}

//fonction changeant l'article, et affichant/masquant l'image selon s'il y en a une ou non
function changeArticle() {
    domTitre = document.getElementById("titreArticle")
    domContenu = document.getElementById("contenuArticle")
    domImage = document.getElementById("imageArticle")
    toutArticle = articles[indexArticles]
    domTitre.innerText = toutArticle.title
    domContenu.innerText = toutArticle.article

    if (toutArticle.image == "") {
        domImage.hidden = true
    }
    else {
        domImage.hidden = false
        domImage.src = "/Medias/" + toutArticle.image
    }
}

//fonction main gérant le fetch des données, et appelant les diverses fontions.
function getArticles() {
    fetch("/api/articles").then((reponse) => reponse.json()).then((data) => {
        articles = data
        //on cache la DOM de l'article s'il n'y a pas d'article
        if (articles.length == 0 && !DOMarticle.hidden) {
            animeSortieArticle(DOMarticle).finished.then(() => {
                DOMarticle.hidden = true
                DOMPasArticle.hidden = false
                setDefaultArticle()
                animeEntreeArticle(DOMPasArticle)
            })
            return
        }
        else if (articles.length == 0)
        {
            setDefaultArticle()
            return
        }
        else if (articles.length >= 1) {   //gestion de l'incrémentation et du bon bouclage
            if (indexArticles == articles.length - 1) {
                indexArticles = -1
            }
            indexArticles++
            domContenu = document.getElementById("contenuArticle")
            //si aucun article n'était affiché
            if (DOMarticle.hidden) {
                indexArticles = 0 //on réinitialise l'index
                animeSortieArticle(DOMPasArticle).finished.then(() => { 
                    DOMPasArticle.hidden = true //on cache le message d'absence d'article
                    changeArticle() //on change l'article,
                    animeEntreeArticle(DOMarticle)//et on affiche le nouveau.
                    DOMarticle.hidden = false
                    checkHeightArticle()
                })
            }
            else if (domContenu.innerText != articles[indexArticles].article) //si l'article à afficher est
            { //différent de l'article affiché, on le change
                animeSortieArticle(DOMarticle).finished.then(() => {
                    changeArticle()
                    animeEntreeArticle(DOMarticle)
                    checkHeightArticle()
                })
            }
        }
    })
}



indexArticles = 0
getArticles()
setInterval(() => getArticles(), 1000 * 60)
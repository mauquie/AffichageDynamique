DOMarticle = document.getElementById("article")
DOMPasArticle = document.getElementById("pasArticle")
contentArticle = null

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

//fonction remettant les tailles par défaut du texte de l'article et du nombre de page
function resetHeights()
{
    document.getElementById("contenuArticle").style.fontSize = "2.5vh"
    document.getElementById("pageNumber").style.fontSize = "2vh"
}

function checkHeightArticle()
{
    //si l'article dépasse 53% de l'écran...
    DOMarticle = document.getElementById("article")
    if ((DOMarticle.clientHeight/window.innerHeight) > 0.50)
    {   
        domContenu = document.getElementById("contenuArticle")//on récupère le texte de l'article,
        DOMpageNumber = document.getElementById("pageNumber")//et le nombre de sa page,
        fontSizeContent = domContenu.style.fontSize//on récupère leur font size
        fontSizeNumber = DOMpageNumber.style.fontSize 
        fontSizeContent = fontSizeContent.substring(0, fontSizeContent.length-2) //dont on ne garde que le nombre
        fontSizeNumber = fontSizeNumber.substring(0, fontSizeNumber.length-2) 
        fontSizeNumber -= 0.01
        fontSizeContent -= 0.01 //on rétrécie le texte et
        DOMpageNumber.style.fontSize = fontSizeNumber + "vh"
        domContenu.style.fontSize = fontSizeContent + "vh"
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
    contentArticle = toutArticle.article

    if (toutArticle.image == "") {
        domImage.hidden = true
    }
    else {
        domImage.hidden = false
        domImage.src = "/Medias/" + toutArticle.image
    }
    DOMpageNumber = document.getElementById("pageNumber")
    DOMpageNumber.innerText = String(indexArticles+1) + "/" + String(articles.length)
    resetHeights()//on reset les tailles aux tailles maximales
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
                    setTimeout(() => {
                        checkHeightArticle() //timeOut pour laisser à l'article le temps de se charger, afin qu'il ait une taille
                    }, 100);                
                })
            }
            else if (contentArticle != articles[indexArticles].article) //si l'article à afficher est
            { //différent de l'article affiché, on le change
                alert(domContenu.innerHTML)
                alert(articles[indexArticles].article)
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
setInterval(() => getArticles(), 1000 * 15)
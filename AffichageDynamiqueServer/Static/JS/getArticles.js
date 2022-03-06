DOMarticle = document.getElementById("article")
DOMPasArticle = document.getElementById("pasArticle")
contentArticle = null
time = 1000 * 10
scrollingDirection = "up"

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

function scrollingArticle(len, occurencesNumber)
{ 
    document.getElementById("article-content").scrollBy(0, len/Math.abs(len))
    occurencesNumber++
    if (occurencesNumber >= Math.abs(len))
    {
        return
    }
    delay = setTimeout(() => {
        scrollingArticle(len, occurencesNumber)
    }, 10)
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

//s'occupe de la gestion du scrolling
function scrollingArticleHandler(reverse)
{
    article = document.getElementById("article-content")
    if (article.scrollHeight * 0.9 >= article.clientHeight && !reverse)
    {
        setTimeout(() => {
            scrollingArticle(article.scrollHeight*0.95 - article.clientHeight, 0)
        }, 5000)
        scrollingDirection = "down"
    }
    else if (reverse)
    {
        setTimeout(() => {
            scrollingArticle(-(article.scrollHeight*0.95 - article.clientHeight), 0)
        }, 5000)
        scrollingDirection = "up"
    }
}
/* Obsolète.
function checkHeightArticle()
{
    DOMimageArticle = document.getElementById("imageArticle")
    //si l'article dépasse 53% de l'écran...
    DOMarticle = document.getElementById("article")
    if ((DOMarticle.clientHeight/window.innerHeight) > 0.50)
    {   
        domContenu = document.getElementById("textArticle")//on récupère le texte de l'article,
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
*/

//fonction changeant l'article, et affichant/masquant l'image selon s'il y en a une ou non
function changeArticle() {
    domTitre = document.getElementById("titreArticle")
    domContenu = document.getElementById("textArticle")
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
    DOMpageNumber = document.getElementById("pageNumber")//on change le nombre de la page actuelle
    DOMpageNumber.innerText = String(indexArticles+1) + "/" + String(articles.length)
}

//fonction main gérant le fetch des données, et appelant les diverses fontions.
function getArticles() {
    // Récupération de la clé unique de l'écran
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);

    fetch("/api/articles?k="+urlParams.get('k')).then((reponse) => reponse.json()).then((data) => {
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
            domContenu = document.getElementById("textArticle")
            domElemArticle = [document.getElementById("titreArticle"), document.getElementById("imageArticle"), document.getElementById("textArticle")]
            //si aucun article n'était affiché
            if (DOMarticle.hidden) {
                indexArticles = 0 //on réinitialise l'index
                animeSortieArticle(DOMPasArticle).finished.then(() => { 
                    DOMPasArticle.hidden = true //on cache le message d'absence d'article
                    changeArticle() //on change l'article,
                    animeEntreeArticle(DOMarticle)//et on affiche le nouveau.
                    DOMarticle.hidden = false
                    scrollingArticleHandler(false)
                }) //event listener pour regarder la taille de l'article
                //que quand l'image est chargée
            }
            else if (contentArticle != articles[indexArticles].article) //si l'article à afficher est
            { //différent de l'article affiché, on le change
                    animeSortieArticle(domElemArticle).finished.then(() => { //on sort l'article actuel
                    changeArticle() //on met le nouveau
                    animeEntreeArticle(domElemArticle) //on anime son entrée
                    scrollingArticleHandler(false) //et on scroll si nécessaire vers le bas
                })
            }
            else if (contentArticle == articles[indexArticles].article)
            { //si on reste sur le même article, il faut alternativement scroll vers le haut / bas
              //et on affiche "1/1" dans la bulle
                if (scrollingDirection == "down")
                {
                    scrollingArticleHandler(true)
                }
                else if (scrollingDirection == "up")
                {
                    scrollingArticleHandler(false)
                }
                DOMpageNumber = document.getElementById("pageNumber")//on change le nombre de la page actuelle
                DOMpageNumber.innerText = String(1) + "/" + String(1)
            }
        }
    })
}



indexArticles = 0
getArticles()
setInterval(() => getArticles(), time)

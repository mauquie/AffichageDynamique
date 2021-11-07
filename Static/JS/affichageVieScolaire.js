DOMarticle = document.getElementById("article")

function animeEntreeArticle()
{
    anime({ 
        targets: DOMarticle,
        translateX: 0, 
        easing: 'cubicBezier(0.110, 0.015, 0.700, 0.115)',
    })
}

function animeSortieArticle()
{
    animationArticle = anime({ 
        targets: DOMarticle,
        translateX: -1000, 
        easing: 'cubicBezier(0.000, 0.175, 0.080, 0.770)',
    })
    return animationArticle
}

function changeArticle()
{
    domTitre = document.getElementById("titreArticle")
    domContenu = document.getElementById("contenuArticle")
    domImage = document.getElementById("imageArticle") 
    toutArticle = articles[indexArticles]
    domTitre.innerText = toutArticle.title
    domContenu.innerText = toutArticle.article
    if (toutArticle.image == "")
    {
        domImage.hidden = true
    }
    else
    {
        domImage.hidden = false
        domImage.src = "/Medias/"+toutArticle.image
    }
}

function getArticles()
{
    fetch("/api/articles").then((reponse)=>reponse.json()).then((data) => {        
        articles = data
        if (articles.length == 0)
        {
            document.getElementById("pasArticle").hidden = false
            DOMarticle.hidden = true
            return
        }
        else
        {
            document.getElementById("pasArticle").hidden = true
            DOMarticle.hidden = false

        }
        domContenu = document.getElementById("contenuArticle")
        if (domContenu.innerText != article.article)
        {
        animeSortieArticle().finished.then(() => 
        {
            changeArticle()
            animeEntreeArticle()
        })
        }
        if (indexArticles == articles.length-1)
        {
            indexArticles = -1
        }
        indexArticles++
    })
}



indexArticles = 0
getArticles()
setInterval(()=>getArticles(), 30000)
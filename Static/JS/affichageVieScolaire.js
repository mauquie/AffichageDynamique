function getArticles()
{
    fetch("/api/articles").then((reponse)=>reponse.json()).then((data) => {        
        articles = data
        if (articles.length == 0)
        {
            document.getElementById("pasArticle").hidden = false
            document.getElementById("article").hidden = true
            return
        }
        else
        {
            document.getElementById("pasArticle").hidden = true
            document.getElementById("article").hidden = false
        }
        domTitre = document.getElementById("titreArticle")
        domContenu = document.getElementById("contenuArticle")
        domImage = document.getElementById("imageArticle") 
        article = articles[i]
        domTitre.innerText = article.title
        domContenu.innerText = article.article
        if (article.image == "")
        {
            domImage.hidden = true
        }
        else
        {
            domImage.hidden = false
            domImage.src = "/Medias/"+article.image
        }
        if (i == articles.length-1)
        {
            i = -1
        }
        i++
    })
}
i = 0
getArticles()
setInterval(()=>getArticles(), 5000)
i = 0
setInterval(()=>{
    fetch("/api/articles").then((reponse)=>reponse.json()).then((data) => {        
        articles = data
        article = articles[i]
        domTitre = document.getElementById("titre")
        domContenu = document.getElementById("contenu")
        domImage = document.getElementById("image") 
        domTitre.innerText = article.title
        domContenu.innerText = article.article
        if (article.image == "")
        {
            domImage.style.visibility = "hidden"
        }
        else
        {
            domImage.style.visibility = "visible"
            domImage.src = "/Medias/"+article.image
        }
        if (i == articles.length-1)
        {
            i = -1
        }
        i++
    })
}, 5000)


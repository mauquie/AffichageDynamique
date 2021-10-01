setInterval(()=>{
    fetch("/api/articles").then((reponse)=>reponse.json()).then((data) => {        
        articles = data
        for(let i = 0; i < articles.length; i++){
            article = articles[i]
            domTitre = document.getElementById("titre")
            domContenu = document.getElementById("contenu")
            domImage = document.getElementById("image") 
            domTitre.innerText = article.title
            domContenu.innerText = article.article
            domImage.src = "/Medias/"+article.image
        }
    })
}, 5000)


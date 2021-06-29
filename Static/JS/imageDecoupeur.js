class imageDecoupeur{
    /**
    *   Classe gérant toutes les mises en lignes d'images.
    *   Elle permet de découper les images, les tourner, etc grâce à la libraire Cropper.js
    * 
    *   @param {HTMLInputElement} imageInput - Element où l'on a choisi la photo à envoyer au serveur
    *   @param {HTMLDivElement} imageUploadBox - Groupe contenant le SVG et la prévisualisation de l'image que l'utilisateur a choisi
    *   @param {HTMLImageElement} [imagePreview = null] - Element IMG où sera affiché la prévisualisation de l'image
    *   @param {SVGSVGElement} [svgImage = null] - Element affiché quand l'utilisateur n'a pas encore choisi de nouvelle valeur
    *   
    */
    constructor(imageInput, imageUploadBox, imagePreview = document.createElement("img"), svgImage = document.createElement("svg")){
        //Attribution et initialisations des éléments HTML utilisés 
        this.imageInput = imageInput
        this.imageUploadBox = imageUploadBox
        this.svgImage = svgImage
        this.imagePreview = imagePreview
        
        this.cropImagePreview = document.getElementById("cropImagePreview")
        this.cropperDiv = document.getElementById("cropper")

        //Initialisation des variables
        this.isImageLoaded = false
        this.imageUploaded;
        this.cropper;

        this._setEvents() //Attributions des fonctions pour les événements adéquats
    }

    _setEvents(){
        /*
        *   Attributions des évenements aux différentes actions de l'utilisateur sur le contenu de la page
        */
        this.imageInput.addEventListener("change", (e) => {
            //Récupération des images depuis l'input
            let image = imageInput.files

            //S'il n'y a pas d'image ou que le FileReader n'est pas disponible
            if (!image.length || !window.FileReader) return;

            //Préparation du reader pour lire l'image
            var reader = new FileReader();
            reader.readAsDataURL(image[0]);

            this.imageUploaded = image[0]

            //Définition de la prévisualisation et de la fenêtre pour découper avec les données du FileReader
            reader.addEventListener("loadend", (e) => {
                this.cropImagePreview.src = e.target.result

                this.isImageLoaded = true
                this.imagePreview.style.backgroundImage = "url(" + e.target.result + ")"

                if(this.cropper != undefined){
                    this.cropper.replace(e.target.result)
                }

                this.imageUploadBox.dataset.bsToggle = "modal"
            })

            //Marsquage du logo et affichage de l'image dans la box de prévisualisation
            this.svgImage.setAttribute("hidden", "true")
            this.imagePreview.hidden = false


        })

        //Attributions des clics aux différentes actions
        this.imageUploadBox.addEventListener("click", () => {
            this.montrerImageInput()
        })

        let saveButton = document.getElementById("saveButton")
        saveButton.addEventListener("click", () => {
            this.saveImage()
        })

        let reset = document.getElementById("reset")
        reset.addEventListener("click", () => {
            this.reset()
        })

        let zoomIn = document.getElementById("zoomIn")
        zoomIn.addEventListener("click", () => {
            this.zoom(0.2)
        })

        let zoomOut = document.getElementById("zoomOut")
        zoomOut.addEventListener("click", () => {
            this.zoom(-0.2)
        })

        let upload = document.getElementById("upload")
        upload.addEventListener("click", () => {
            this.changeImage()

        })

        let rotate = document.getElementById("rotate")
        rotate.addEventListener("click", () => {
            this.rotate(45)
        })

        let remove = document.getElementById("remove")
        remove.addEventListener("click", () => {
            this.delete()
        })
    }

    montrerImageInput(){
        /**
        *   Fonction appelé quand on appuie sur l'élément pour choisir une image
        */
        if(!this.isImageLoaded){
            this.imageInput.click()

        } else {
            if(this.cropper === undefined){
                setTimeout(() => {
                        this._createCropper()
                }, 1000)
            }
            
        }
    }

    _createCropper(){
        /**
         *  Fonction créant le découpeur et l'initialisant dans la fenêtre Modal
         */
        let width = this.cropperDiv.offsetWidth;
        
        this.cropper = new Cropper(this.cropImagePreview, { //Options du découpeur
            dragMode: 'move',
            minContainerWidth: width,
            minContainerHeight: width * 9 /16, //Toujours le même ratio 16:9
            aspectRatio: 16 / 9,
            initialAspectRatio: 16 / 9,
            autoCropArea: 1,
            toggleDragModeOnDblclick: false,

            ready: function() { //Masquage du logo de chargement
                let loadingSpiner = document.getElementById("loadingSpiner")
                loadingSpiner.hidden = true
            },

        }) 
    }

    saveImage(){
        /**
         *  Fonction s'occupant de sauvegarder l'image dans l'input général et d'appliqué les modifications à la prévisualisation 
         */
        let croppedCanva = this.cropper.getCroppedCanvas() //Récupération des données du découpage

        if(croppedCanva !== null){ //Si il y a bien des données

            //Exportation

            croppedCanva.toBlob((blob) => {
                //Lecture des données récupérées
                let reader = new FileReader();
                reader.readAsDataURL(blob);

                let imagePreview = this.imagePreview
                let imageInput = this.imageInput

                reader.onloadend = (e) => { //Application aux différents éléments 
                    imagePreview.style.backgroundImage = "url(" + e.target.result + ")"
                    
                    //Transmission de la nouvelle image (découpée ou autre) à l'input de départ
                    let file = new File([blob], imageInput.files[0].name, {type: imageInput.files[0].type, lastModified:new Date().getTime()});
                    let container = new DataTransfer();
                    container.items.add(file);
                    imageInput.files = container.files;
                }
            })
        } else { //Si en l'occurrence il n'y a pas de données exportées (c'est à dire que l'image a été supprimé)
            this.imageInput.value = "" //On supprime l'image dans l'input
        }
        


    }

    changeImage(){
        /**
         *  Fonction s'occupant de changer l'image actuellement choisi
         */
        this.isImageLoaded = false
        this.montrerImageInput()
    }

    rotate(number){
        /**
         *  Fonction s'occupant de faire la rotation de l'image
         * 
         *  @param {number} number - Nombre de degrés pour tourner la photo
         */
        this.cropper.rotate(number)
    }

    reset(){
        /**
         *  Fonction s'occupant de reinitialiser les paramètres rentrés (le zoom, le deplacement etc) du découpeur
         */
        this.cropper.reset()
    }

    zoom(number){
        /**
         *  Fonction s'occupant de zoomer dans la photo
         *  @param {number} number - Nombre à utiliser pour la puissance du zoom
         */
        this.cropper.zoom(number)
    }

    delete(){
        /**
         *  Fonction s'occupant de supprimer toutes les traces de l'image en cours de modification
         */
        this.cropper.destroy()
        this.saveImage()

        this.svgImage.removeAttribute("hidden")
        this.imagePreview.style.backgroundImage = ""
        this.imageUploadBox.dataset.bsToggle = ""
        this.imagePreview.hidden = true
        this.isImageLoaded = false
    }
}
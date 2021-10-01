class List {
    /**
     *  Classe s'occupant de gérer la sélection d'un objet dans une table (DomElement) donnée et la mise à jour
     *  automatique du titre de l'objet sélectionné dans un DomElement et la mise à jour du texte toggle en fonction de si
     *  l'objet sélectionné à une particularité (présence d'une classe précise dans le <tr>).
     * 
     *  @Params
     *      objects {List} - Liste des éléments <tr> du tableau
     *      title {DomElement} - Element DOM qui prendra le nom l'objet sélectionné 
     *      button {DomButton} - Bouton qui changera de style en fonction de l'objet sélectionné
     *      ?classOfDisabledObject {String} - classe de l'objet (dans le tableau) qui sera mit en évidence
     *      ?activeMessage {String} - Texte qui sera affiché sur le bouton quand l'objet sélectionné est en évidence
     *      ?disableMessage {String} - Texte qui sera affiché sur le bouton quand l'objet sélectionné n'est pas en évidence
     */
    constructor(objects, title, button, classOfDisabledObject = "table-warning", activeMessage = "Montrer", disableMessage = "Cacher"){
        this.objects = objects
        this.selected = undefined
        this.title = title
        this.button = button
        this.activeMessage = activeMessage
        this.disableMessage = disableMessage
        this.classOfDisabledObject = classOfDisabledObject
        
        //Association des lignes du tableau avec les fonctions
        this._associateObjectFunctions()
    }

    _associateObjectFunctions(){
        /*
        *   Association de chaque ligne du tableau contenant les articles aux fonctions
        *   gérant les boutons et les lignes ditent "active" (sélectionné)
        */

        //Affectation de l'évenement "click" à chaque ligne du tableau contenant les articles
        for(let i = 0; i < this.objects.length ; i++){
            this.objects[i].addEventListener("click", () => {
                this._toggleObjectActive(this.objects[i])
                this._toggleActions(this.selected)
            })
        }
    }

    _toggleObjectActive(object){
        /**
         *  Association du clic sur un objet avec la mise en évidence d'une ligne du tableau
         */
        
        //Si l'user à déjà sélectionné un objet
        if(this.selected !== undefined){
            //Suppression du style de mise en évidence pour l'ancien objet sélectionné
            let classList = this.selected.classList.value.split(" ")
            classList.pop()
            this.selected.classList.value = classList.join(" ")
                    
        }
                
        //Mise en évidence du nouvel objet
        this.selected = object
        this.selected.classList.value += " table-active"

        //Creation d'un evenement quand on sélectionne un objet dans la liste
        this.selectionEvent = new CustomEvent("selection", {
            detail: this.selected,
            bubbles: true,
            cancelable: true,
            composed: false,
        })

        //Envoie de l'evenement
        document.dispatchEvent(this.selectionEvent)
    }

    _toggleActions() {
        /*
        *   Fonction affichant les boutons quand l'utilisateur selectionne un objet
        *   et qui modifie le bouton toggle en fonction de si objet est actuellement
        *   "activé" ou "désactivé"
        */
        
        //Modification du texte affichant le nom de l'objet selectionné
        this.title.innerText = this.selected.children[0].innerText

        //Changement du texte du bouton toggle
        if(this.selected.className.indexOf(this.classOfDisabledObject) != -1){
            //Si l'objet est en évidence
            this.button.innerHTML = this.activeMessage
            this.button.className = "btn btn-outline-success"

        } else {
            //Si l'objet n'est pas en évidence
            this.button.innerHTML = this.disableMessage
            this.button.className = "btn btn-outline-warning"
        }
    }
}
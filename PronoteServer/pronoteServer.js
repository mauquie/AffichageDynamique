/**
 * Fichier créant et connectant ce serveur au serveur de pronote et qui
 * renvoie les informations quand on demande à l'api
 */

const pronote = require('@dorian-eydoux/pronote-api');
const http = require("http")
const dotenv = require("dotenv").config({path: "../.env"})

const url = 'https://0820021c.index-education.net/pronote/';
const username = process.env.PRONOTE_USERNAME;
const password = process.env.PRONOTE_PASSWORD;
const cas = 'ac-toulouse';

var server = undefined;

async function getSession() {
    /**
     * Fonction créant la session pronote nécessaire pour récupérer ces données 
     * 
     * @returns
     * session - la session pronote
     */
    const session = await pronote.login(url, username, password, cas);

    session.setKeepAlive(true)

    return session
}

async function getMenus(session, date = new Date()) {
    /**
        Fonction recupérant les menus à une date donnée 

        @params
        session - La session pronote actuelle
        ?date - La date à laquelle on veut récupérer les données

        @returns
        list - Retourne la liste des menus à la date demandée
    */
    date.setDate(date.getDate() - 1)
    return await session.menu(from = date)
}

async function getEdt(session, date = new Date(2022, 0, 20)) {
    /**
        Fonction recupérant l'emploi du temps à une date donnée 

        @params
        session - Le session pronote actuelle
        ?date - la date à laquelle on veut récupérer les données

        @returns
        list - Retourne la liste des cours de la date demandée
    */
    let today = new Date()
    today.setDate(date.getDate() - 1)
    return await session.timetable(from = today, to = date)
}

function gestionServeur(req, res, session) {
    /**
     * Fonction gérant les requetes sur le serveur, elle s'occupe de renvoyer les menus sous forme
     * JSON quand on demande l'url /menus par exemple
     * 
     * @params
     * req: requête initiale
     * res: reponse à envoyer au serveur
     * session: session pronote
     */

    //Si on veut les menus
    if (req.url == "/menus") {

        //On récupère les menus via la fonction getMenus avec notre session en paramètre
        getMenus(session)
            .then((menus) => {

                //Une fois qu'on a les menus on les renvoie sous forme JSON
                res.writeHead(200, {
                    'Content-Type': 'application/json'
                })

                res.write(JSON.stringify({
                    'data': menus
                }))
	            console.log(generateDate() + "Menus récupérés :")
                console.log(menus)
                res.end()
            })
            .catch(err => {
                gestionError(err, res)
            })

        //Si on veut les menus
    } else if (req.url == "/edt") {

        //On récupère l'emploi du temps du jours via la fonction getEdt avec notre session en paramètre
        getEdt(session)
            .then((edt) => {

                //Une fois qu'on a l'emploi du temps on le renvoie sous forme JSON
                res.writeHead(200, {
                    'Content-Type': 'application/json'
                })

                res.write(JSON.stringify({
                    'data': edt
                }))
                console.log(generateDate() + "Emploi du temps récupérés :")
                console.log(edt)
                res.end()
            })
            .catch(err => {
                gestionError(err, res)
            })
    }
}

function generateDate(){
    /**
     * Génère un string contenant la date et l'heure au moment précis où
     * la fonction est exécutée
     * 
     * @returns
     * string - Date sous format [AAAA:MM:JJ HH:MM:SS]
     */
    let ts = Date.now()

    let date_ob = new Date(ts);
    let date = date_ob.getDate();
    let month = date_ob.getMonth() + 1;
    let year = date_ob.getFullYear();

    let hours = date_ob.getHours();
    let minutes = date_ob.getMinutes();
    let seconds = date_ob.getSeconds();

    // Affiche la date sous la forme [AAAA/MM/JJ HH:MM:SS]
    return "[" + year + "/" + month + "/" + date + " " + hours + ":" + minutes + ":" + seconds + "]"
}

function gestionError(err, res){
    /**
     * Gère les erreurs quand elle arrive, c'est à dire les notifie dans la
     * console, redémarre la connexion avec pronote si nécessaire et renvoie 
     * une liste vide de donnée
     */
    console.error(generateDate() + "Error from pronote")
    console.error(err)

    if(err.code == 5){
        console.log(generateDate() + "Rebooting the server")
        loadSession()
    }

    res.writeHead(200, {
        'Content-Type': 'application/json'
    })

    res.write(JSON.stringify({
        'data': []
    }))

    res.end()
}

function loadSession(){
    /**
     * Charge le serveur sur le port 5000 une fois la connexion avec pronote réussi
     */
    if (server !== undefined){
        server.close()
    }
    //Création de la session pronote
    getSession()
        .then((session) => {
            //Une fois que la session est crée on peut créer le serveur web
            server = http.createServer((req, res) => {
                gestionServeur(req, res, session)
            })

            server.listen(5000)
            console.log(generateDate() + "Serveur lancé sur le port 5000")
        })
        .catch((err) => {
            console.error(generateDate() + "Ups pronote connection error :")
            console.error(err)
        })
}

loadSession()

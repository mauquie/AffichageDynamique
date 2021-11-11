const pronote = require('@dorian-eydoux/pronote-api');
const http = require("http")


const url = 'https://0820021c.index-education.net/pronote/';
<<<<<<< HEAD
const username = 'marc.betous';
const password = 'itchibiegourou';
=======
const username = 'elowan.harnisch';
const password = 'mindstorms';
>>>>>>> d3ed354112fccc2405889a30735c11d95f13bcf7
const cas = 'ac-toulouse';


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

        @param
        session - Le session pronote actuelle
        ?date - la date à laquelle on veut récupérer les données

        @return
        list - Retourne la liste des menus à la date demandée
    */
    date.setDate(date.getDate() - 1)
    return await session.menu(from = date)
}

async function getEdt(session, date = new Date()) {
    /**
        Fonction recupérant l'emploi du temps à une date donnée 

        @param
        session - Le session pronote actuelle
        ?date - la date à laquelle on veut récupérer les données

        @return
        list - Retourne la liste des cours de la date demandée
    */
    date.setDate(date.getDate() - 1)
    return await session.timetable(from = date)
}

function gestionServeur(req, res, session) {
    /**
     * Fonction gérant les requetes sur le serveur, elle s'occupe de renvoyer les menus sous forme
     * JSON quand on demande l'url /menus par exemple
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
	            console.log(menus)
                res.end()
            })
            .catch(err => {
                console.error("Ups, error : ")
                console.error(err)

                //Une fois qu'on a l'emploi du temps on le renvoie sous forme JSON
                res.writeHead(200, {
                    'Content-Type': 'application/json'
                })

                res.write(JSON.stringify({
                    'data': []
                }))

                res.end()
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
                console.log(edt)
                res.end()
            })
            .catch(err => {
                console.error("Ups, error : ")
                console.error(err)

                //Une fois qu'on a l'emploi du temps on le renvoie sous forme JSON
                res.writeHead(200, {
                    'Content-Type': 'application/json'
                })

                res.write(JSON.stringify({
                    'data': []
                }))

                res.end()
            })
    }
}

//Création de la session pronote
getSession()
    .then((session) => {
        //Une fois que la session est crée on peut créer le serveur web
        var server = http.createServer((req, res) => {
            gestionServeur(req, res, session)
        })

        server.listen(5000)
        console.log("Serveur lancé sur le port 5000")
    })
    .catch((err) => {
        console.log("Ups pronote connection error :")
        console.error(err)
    })

def getEnv(location = ".env"):
    """
        Lit le fichier .env dans le repertoire choisi et renvoie un dictionnaire
        avec les valeurs

        @param:
            ?location(string) - Localisation du .env

        @return
            dict - Dictionnaire avec les valeurs
    """
    #Ouverture du fichier
    env = open(location)

    #Lecture des lignes => Liste des lignes
    envListBase = env.readlines()

    envDict = {}

    #Pour chaque ligne
    for line in envListBase:
        #On enleve le retour à la ligne s'il y en a un
        line = line.split("\n")[0]

        #Si la ligne n'est pas vide
        if line != "":
            #On separe la ligne en deux au niveau de =
            line = line.split("=")

            #On affecte le nom de la variable à la valeur
            # De : DB_PORT = 5432
            # A : {"DB_PORT": 5432}
            envDict[line[0]] = line[1]

    return envDict
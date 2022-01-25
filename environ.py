def getEnv(location = ".env"):
    """
    Lit le fichier .env dans le repertoire choisi et renvoie un dictionnaire
    avec les valeurs. Si il n'est pas trouvé alors il renvoie un dictionnaire vide

    Args:
        location (str, optionnel): Localisation du .env
        
    Returns:
        dict: Dictionnaire avec les valeurs
    """
    #Ouverture du fichier
    try:
    	env = open(location)
    
    except FileNotFoundError:
    	return {}
    	
    else:
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

#
#  Created by Elowarp on 09/01/2020
#
#  Fichier de commande Django,
#  Ajoute toutes les valeurs par défaut depuis le fichier data.json
#

from django.core.management.base import BaseCommand
from ApiServer.models import InfoTypes, MealParts, GroupsExtend
from django.contrib.auth.models import Permission, ContentType
import json 

class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'Ajout des valeurs de base pour le bon fonctionnement du serveur'

    def _create_tags(self):
        print("Ajout des valeurs par défaut à la base de données")
        # Récupération des permissions et groupes à créer
        f = open('../data.json')
        data = json.load(f)

        # Ajout des types d'informations
        for infotype in data["infotypes"]:
            infoTypeObj = InfoTypes.objects.get_or_create(name=infotype)[0]
            infoTypeObj.save()

        # Ajout des différentes parties des repas
        for part in data["mealparts"]:
            mealPart = MealParts.objects.get_or_create(name=part)[0]
            mealPart.save()

        
        # Ajout des différentes permissions données
        for perm in data["perms"]:
            # Soit on récupère l'object soit on le créer 
            # Ca evite les erreurs du type "La clé (..) est déjà trouvée dans la BDD" au cas ou on a déjà populate la BDD
            permObject = Permission.objects.get_or_create(name=perm["name"], codename=perm["codename"], content_type=ContentType(pk=perm["contenttype"]))[0]
            permObject.save()


        actions = ["add", "change", "delete", "view"]

        # Ajout des groupes donnés
        for key, value in data["groups"].items():
            # On récupère ou créer un nouveau groupe avec ces valeurs
            currentGroup = GroupsExtend.objects.get_or_create(name=key, level=value["level"])[0]
            currentGroup.save()

            # Ajout des permissions au groupe
            for perm in value["perms"]:
                # Pour chaque permission, on a 4 actions 
                # Ajouter, Changer, Voir et Supprimer
                # Ajout les 4 actions par permission
                for action in actions:
                    # Formatage du codename de la permission
                    # Ex : add_articles
                    code = action + "_" + perm
                    
                    # Vérification que la permission qu'on ajoute ne fait pas 
                    # partie des permissions créees haut dessus, si c'est le cas, la permission n'a pas
                    # d'action elle se suffit à elle même
                    #  Ex : manage_screens (Existe, on vient de la créer)
                    #       add_manage_screens (N'existe pas)
                    for permDict in data["perms"]:
                        if (perm == permDict["codename"]):
                            code = perm 
                            break

                    # Récupération et ajout de la permission au groupe
                    permission = Permission.objects.all().filter(codename=code)[0]
                    currentGroup.permissions.add(permission)

            currentGroup.save()

        f.close()
        print("Fait")

    def handle(self, *args, **options):
        self._create_tags()
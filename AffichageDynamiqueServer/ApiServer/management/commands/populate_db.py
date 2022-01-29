#
#  Created by Elowarp on 09/01/2020
#
#  Fichier de commande Django,
#  Ajoute toutes les valeurs par défaut depuis le fichier data.json
#

from django.core.management.base import BaseCommand
from ApiServer.models import Absents, InfoTypes, Informations, MealParts, GroupsExtend, Teachers, Users, Articles
from django.contrib.auth.models import Permission, ContentType
import json 
import datetime

class Command(BaseCommand):
    args = ''
    help = 'Ajout des valeurs de base pour le bon fonctionnement du serveur'

    def add_arguments(self, parser):
        parser.add_argument(
            "-a",
            "--add_additionals",
            action="store_true",
            help="Ajoute les valeurs additionnels pour faciliter le debug"    
        )

    def _add_additionals(self):
        # Vérification qu'au moins 1 user existe
        users = Users.objects.all()
        if len(users) < 1:
            print("Il faut créer au moins un utilisateur avec d'utiliser cette commande")
            return

        # Chargement des données
        f = open('../data.json')
        data = json.load(f)
    
        # Utilisation du premier user en tant que auteur des objets crées apres
        user = users.filter(pk=1)[0]

        # Ajout des informations
        for info in data["informations"]:
            information = Informations.objects.get_or_create(
                message=info["message"],
                is_shown=info["is_shown"],
                author=user,
                date_end=datetime.datetime.now(),
                type=InfoTypes.objects.filter(name=info["type"])[0]
            )[0]
            information.save()

        # Ajout des articles
        for articleData in data["articles"]:
            article = Articles.objects.get_or_create(
                title=articleData["title"],
                content=articleData["content"],
                date_end=datetime.datetime.now(),
                author=user,
                date_last_modif=datetime.datetime.now(),
                user_last_modif=user,
                is_shown=articleData["is_shown"]
            )[0]

            article.save()

        # Ajout des profs absents
        for abs in data["absents"]:
            teacher = Teachers.objects.get_or_create(name=abs["teacher"])[0]
            teacher.save()

            absent = Absents.objects.get_or_create(
                teacher=teacher,
                date_start=datetime.datetime.now(tz=datetime.timezone.utc),
                date_end=datetime.datetime.now(tz=datetime.timezone.utc).replace(hour=datetime.datetime.now(tz=datetime.timezone.utc).hour - 23)
            )[0]
            absent.save()

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
                    # Ex : manage_screens (Existe, on vient de la créer)
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
        if(options['add_additionals']):
            self._add_additionals()

        else:
            self._create_tags()
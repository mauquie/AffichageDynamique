"""
Gère de toute la partie "twitter" du projet
"""

import tweepy
import AffichageDynamique.settings as settings

client = tweepy.Client(bearer_token=settings.TWITTER_BEARER_TOKEN)

def getLastTweets():
    """
    Récupère les tweets du compte lycee bourdelle, avec la limite de 5 maximum

    Returns:
        dict: Données des tweets et des métadonnées (comme le plus récent ou autre)

    Example:

        .. code-block:: JSON
        
            {
                "data": [
                    {
                        "text": "ERASMUS avec les collèges @Col_Despeyrous ...",
                        "created_at": "2022-01-21T09:47:27Z"
                    },
                    {
                        "text": "ERASMUS+ LP BOURDELLE: signatures des con ...",
                        "created_at": "2022-01-13T10:26:51Z"
                    },
                ],
                "meta": {
                    "oldest_id": "1471875800865689601",
                    "newest_id": "1484462637899526147",
                    "result_count": 5
                }
            }
    """
    #Récupère les données depuis twitter
    response = client.get_users_tweets(id=961221886733639682, max_results=5, expansions="referenced_tweets.id", tweet_fields="created_at")
    
    #Formatage des données à renvoyer
    if not response.errors:
        meta = dict(response.meta)
        print(meta)
        return {
            "data": [
                {
                    "text": tweet.text,
                    "created_at": tweet.created_at,
                } for tweet in response.data
            ],
            "meta": {
                "oldest_id": meta["oldest_id"],
                "newest_id": meta["newest_id"],
                "result_count": meta["result_count"]
            },
        }

    return {}
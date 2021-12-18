"""
Fichier s'occupant de récupérer les tweets du twitter du lycéee
"""

import tweepy
import AffichageDynamique.settings as settings

client = tweepy.Client(bearer_token=settings.TWITTER_BEARER_TOKEN)

def getLastTweets():
    #Fonction récupérant les tweets du compte lycee bourdelle, avec la limite max de 5
    response = client.get_users_tweets(id=961221886733639682, max_results=5, expansions="referenced_tweets.id", tweet_fields="created_at")
    
    #Formatage des données à renvoyer
    if not response.errors:
        return {
            "data": [
                {
                    "text": tweet.text,
                    "created_at": tweet.created_at,
                } for tweet in response.data
            ],
            "meta": dict(response.meta),
        }

    return {}
from django.urls import path
from . import views


#Urls concernant le serveur servant d'API
urlpatterns = [
    path('articles', views.getArticles),
    path('infos', views.getInfos),
    path('sondages', views.getSurveys),
    path('displays', views.getDisplays),
    path('meals', views.getMeals),
    path('profsAbs', views.getProfsAbs),
    path('postVote', views.postVote),
    path('tweets', views.getTweets),
    path('meteo', views.getMeteo)
]
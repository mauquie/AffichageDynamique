from django.urls import path
from . import views


#Urls concernant le serveur servant d'API
urlpatterns = [
    path('articles', views.getArticles),
    path('infos', views.getInfos),
    path('sondages', views.getSurveys)
]
from django.urls import path
from . import views as urls


#Urls concernant le serveur servant d'API
urlpatterns = [
    path('', urls.index)
]
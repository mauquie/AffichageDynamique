from django.urls import path
from . import views as urls


#Urls concernant le serveur Web (celui utilisé par des êtres humains)
urlpatterns = [
    path("", urls.index)
]
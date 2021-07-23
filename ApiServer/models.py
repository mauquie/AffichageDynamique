from django.db import models
from django.contrib import admin
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group
from django.db.models.deletion import DO_NOTHING

# Les modèles nécéssaires pour la base de données. Les modèles pour l'administration sont créées en dessous.

class User(AbstractUser):
    profile_picture = models.ImageField(upload_to="")

class Article(models.Model):
    title = models.CharField(max_length=100)
    article = models.CharField(max_length=4000)
    image = models.ImageField(upload_to="")
    creation_date = models.DateField(auto_created=True)
    expiration_date = models.DateField(auto_created=True)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='author')
    modification_date = models.DateField(auto_created=True)
    last_edit_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)

class Page(models.Model):
    url = models.CharField(max_length=30)
    description = models.CharField(max_length=100)

class Display(models.Model):
    name = models.CharField(max_length=100)
    page = models.ForeignKey(Page, on_delete=models.DO_NOTHING)

# Tous les modèles administrateurs

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'article', 'image', 'creation_date', 'expiration_date', 'author', 'modification_date', 'last_edit_by')
    list_filter = ('title', 'author', 'creation_date', 'expiration_date')
    search_fields = ['title', 'author', 'creation_date']

class PageAdmin(admin.ModelAdmin):
    list_display = ('url', 'description')
    list_filter = ('url', 'description')
    search_fields = ['url']

class DisplayAdmin(admin.ModelAdmin):
    list_display = ('name', 'page')
    list_filter = ('name', 'page')
    search_fields = ['name']
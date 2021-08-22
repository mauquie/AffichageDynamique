from enum import auto
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group
from django.db.models.deletion import DO_NOTHING

# Les modèles nécéssaires pour la base de données. Les modèles pour l'administration sont créées en dessous.

class User(AbstractUser):
    profile_picture = models.ImageField(upload_to="Medias/User/profile_picture/")

class Article(models.Model):
    title = models.CharField(max_length=100)
    article = models.CharField(max_length=4000)
    image = models.ImageField(upload_to="Medias/Articles/", blank=True)
    creation_date = models.DateField(auto_created=True)
    expiration_date = models.DateField(auto_created=True)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='author')
    modification_date = models.DateField(auto_created=True)
    last_edit_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    perm_group = models.ForeignKey(Group, on_delete=models.DO_NOTHING)
    is_shown = models.BooleanField()

class Page(models.Model):
    localisation = models.FileField()
    description = models.CharField(max_length=100)

class Display(models.Model):
    name = models.CharField(max_length=100)
    page = models.ForeignKey(Page, on_delete=models.DO_NOTHING)

class Survey(models.Model):
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    description = models.CharField(max_length=300)
    link = models.CharField(max_length=300)
    creation_date = models.DateField(auto_created=True)
    expiration_date = models.DateField()
    is_shown = models.BooleanField()
    
class InfoType(models.Model):
    name = models.CharField(max_length=30)

class Info(models.Model):
    type = models.ForeignKey(InfoType, on_delete=models.DO_NOTHING)
    message = models.CharField(max_length=150)
    is_shown = models.BooleanField()
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    creation_date = models.DateField(auto_created=True)
    expiration_date = models.DateField()

# Tous les modèles administrateurs

class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'username', 'email', 'password', 'last_login', 'date_joined', 'is_active', 'is_staff', 'is_superuser', 'profile_picture')
    list_filter = ('first_name', 'last_name', 'username', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ['first_name', 'username', 'is_active', 'is_staff', 'is_superuser']
    
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

class SurveyAdmin(admin.ModelAdmin):
    list_display = ('description', 'link', 'author', 'creation_date', 'expiration_date', 'is_shown')
    list_filter = ('description', 'author', 'creation_date', 'is_shown')
    search_fields = ['description', 'author', 'creation_date', 'is_shown']
    
class InfoTypeAdmin(admin.ModelAdmin):
    list_display = ('name')
    list_filter = ('name')
    search_fields = ['name']

class InfoAdmin(admin.ModelAdmin):
    list_display = ('message', 'type', 'author', 'creation_date', 'expiration_date', 'is_shown')
    list_filter = ('message', 'type', 'author', 'creation_date', 'is_shown')
    search_fields = ['message', 'type', 'author', 'creation_date', 'is_shown']
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import AbstractUser, Group

# Les modèles nécéssaires pour la base de données. Les modèles pour l'administration sont créées en dessous.

class GroupExtend(Group):
    level = models.IntegerField()

class User(AbstractUser):
    profile_picture = models.ImageField(upload_to="User/profile_picture/")

class Article(models.Model):
    title = models.CharField(max_length=100)
    article = models.CharField(max_length=4000)
    image = models.ImageField(upload_to="Articles/", blank=True)
    creation_date = models.DateField(auto_now_add=True)
    expiration_date = models.DateField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author', auto_created=True)
    modification_date = models.DateField(auto_now_add=True)
    last_edit_by = models.ForeignKey(User, on_delete=models.CASCADE, auto_created=True)
    perm_group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)
    is_shown = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Page(models.Model):
    filename = models.CharField(max_length=100,null=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.description

class Display(models.Model):
    name = models.CharField(max_length=100)
    code_name = models.CharField(max_length=100, default="")
    page = models.ForeignKey(Page, on_delete=models.CASCADE, null=True)


class Survey(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=300)
    link = models.CharField(max_length=300)
    creation_date = models.DateField(auto_now_add=True)
    expiration_date = models.DateField()
    is_shown = models.BooleanField(default=True)

    def __str__(self):
        return self.description
    
class InfoType(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Info(models.Model):
    type = models.ForeignKey(InfoType, on_delete=models.CASCADE)
    message = models.CharField(max_length=150)
    is_shown = models.BooleanField(default=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateField(auto_now_add=True)
    expiration_date = models.DateField()

    def __str__(self):
        return self.message


# Modèles correpondants à Pronote
class ProfAbsent(models.Model):
    teacher = models.CharField(max_length=100)
    debut = models.DateTimeField()
    fin = models.DateTimeField()

    def __str__(self):
        return "{}, {} à {}".format(self.teacher, self.debut, self.fin)

class PartieDuRepas(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Aliment(models.Model):
    name = models.CharField(max_length=100)
    partie_du_repas = models.ForeignKey(PartieDuRepas, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class Repas(models.Model):
    repas_midi = models.BooleanField()
    date = models.DateField()
    aliments_du_repas = models.ManyToManyField(Aliment)

    def __str__(self):
        if self.repas_midi:
            titre = "{} - Midi".format(self.date)

        else:
            titre = "{} - Soir".format(self.date)

        return titre 

class Sondage(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.CharField(max_length=50)
    date_creation = models.DateTimeField(auto_created=True, auto_now=True)
    date_fin = models.DateTimeField()
    est_affiche = models.BooleanField()

    def __str__(self):
        return self.question

class Reponse(models.Model):
    sondage = models.ForeignKey(Sondage, on_delete=models.CASCADE)
    text = models.CharField(max_length=50)

    def __str__(self):
        return self.text


# Tous les modèles administrateurs

class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'username', 'email', 'password', 'last_login', 'date_joined', 'is_active', 'is_staff', 'is_superuser', 'profile_picture')
    list_filter = ('first_name', 'last_name', 'username', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ['first_name', 'username', 'is_active', 'is_staff', 'is_superuser']
    
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'article', 'image', 'creation_date', 'expiration_date', 'author', 'modification_date', 'last_edit_by', 'perm_group')
    list_filter = ('title', 'author', 'creation_date', 'expiration_date')
    search_fields = ['title', 'author', 'creation_date']

class PageAdmin(admin.ModelAdmin):
    list_display = ('description', 'filename')
    list_filter = ('description', 'filename')
    search_fields = ['filename']

class DisplayAdmin(admin.ModelAdmin):
    list_display = ('name', 'code_name', 'page')
    list_filter = ('name', 'page')
    search_fields = ['name', 'code_name']

class SurveyAdmin(admin.ModelAdmin):
    list_display = ('description', 'link', 'author', 'creation_date', 'expiration_date', 'is_shown')
    list_filter = ('description', 'author', 'creation_date', 'is_shown')
    search_fields = ['description', 'author', 'creation_date', 'is_shown']
    
class InfoTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ['name']

class InfoAdmin(admin.ModelAdmin):
    list_display = ('message', 'type', 'author', 'creation_date', 'expiration_date', 'is_shown')
    list_filter = ('message', 'type', 'author', 'creation_date', 'is_shown')
    search_fields = ['message', 'type', 'author', 'creation_date', 'is_shown']

class RepasAdmin(admin.ModelAdmin):
    list_display = ('repas_midi', 'date')
    list_filter = ('repas_midi', 'date', 'aliments_du_repas')
    search_fields = ['repas_midi', 'date', 'aliments_du_repas']

class AlimentRepas(admin.ModelAdmin):
    list_display = ('name', 'partie_du_repas')
    list_filter = ('name', 'partie_du_repas')
    search_fields = ['name', 'partie_du_repas']

class PartieDuRepasAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name', )
    search_fields = ['name']

class ProfAbsentAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'debut', 'fin')
    list_filter = ('teacher', 'debut', 'fin')
    search_fields = ['teacher']

class SondageAdmin(admin.ModelAdmin):
    list_display = ("question", "author")
    list_filter = ('question', "author", "date_creation", "date_fin", "est_affiche")
    search_fields = ['question', 'author']

class ReponseAdmin(admin.ModelAdmin):
    list_display = ("sondage", "text")
    list_filter = ("sondage", "text")
    search_fields = ['sondage', "text"]
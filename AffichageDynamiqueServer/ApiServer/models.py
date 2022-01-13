from django.db import models
from django.contrib import admin
from django.contrib.auth.models import AbstractUser, Group

# Les modèles nécéssaires pour la base de données. Les modèles pour l'administration sont créées en dessous.

class GroupsExtend(Group):
    level = models.IntegerField()

class Users(AbstractUser):
    profile_picture = models.ImageField(upload_to="Users/profile_pictures/", null=True, default="")

    def __str__(self):
        return self.username

class Articles(models.Model):
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=700)
    image = models.ImageField(upload_to="Articles/", blank=True)
    date_creation = models.DateField(auto_now_add=True)
    date_end = models.DateField()
    author = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='author', auto_created=True)
    date_last_modif = models.DateField(auto_created=True, auto_now=True)
    user_last_modif = models.ForeignKey(Users, on_delete=models.CASCADE, auto_created=True)
    is_shown = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Pages(models.Model):
    filename = models.CharField(max_length=100)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.description

class Screens(models.Model):
    name = models.CharField(max_length=100)
    code_name = models.CharField(max_length=100, default="")
    page = models.ForeignKey(Pages, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

class InfoTypes(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Informations(models.Model):
    type = models.ForeignKey(InfoTypes, on_delete=models.CASCADE)
    message = models.CharField(max_length=150)
    is_shown = models.BooleanField(default=False)
    author = models.ForeignKey(Users, on_delete=models.CASCADE)
    date_creation = models.DateField(auto_now_add=True)
    date_end = models.DateField()

    def __str__(self):
        return self.message


# Modèles correpondants à Pronote
class Teachers(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Absents(models.Model):
    teacher = models.ForeignKey(Teachers, on_delete=models.CASCADE)
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()

    def __str__(self):
        return "{}, {} à {}".format(self.teacher, self.date_start, self.date_end)

class MealParts(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Foods(models.Model):
    name = models.CharField(max_length=100)
    meal_part = models.ForeignKey(MealParts, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class Meals(models.Model):
    is_midday = models.BooleanField()
    date = models.DateField()
    to_eat = models.ManyToManyField(Foods)

    def __str__(self):
        if self.is_midday:
            titre = "{} - Midi".format(self.date)

        else:
            titre = "{} - Soir".format(self.date)

        return titre 

class Surveys(models.Model):
    author = models.ForeignKey(Users, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    date_creation = models.DateField(auto_now_add=True)
    date_end = models.DateField()
    is_shown = models.BooleanField(default=False)

    def __str__(self):
        return self.subject

class Answers(models.Model):
    survey = models.ForeignKey(Surveys, on_delete=models.CASCADE)
    answer = models.CharField(max_length=50)

    def __str__(self):
        return self.answer

class Votes(models.Model):
    author = models.ForeignKey(Users, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answers, on_delete=models.CASCADE)
    survey = models.ForeignKey(Surveys, on_delete=models.CASCADE)

    def __str__(self):
        return self.author.username + " - " + self.answer.answer

# Tous les modèles administrateurs

class UsersAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'password', 'last_login', 'date_joined', 'is_active', 'is_staff', 'is_superuser', 'profile_picture')
    list_filter = ('username', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ['username', 'first_name', 'is_active', 'is_staff', 'is_superuser']
    
class ArticlesAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'image', 'date_creation', 'date_end', 'author', 'date_last_modif', 'user_last_modif')
    list_filter = ('title', 'author', 'date_creation', 'date_end')
    search_fields = ['title', 'author', 'date_creation']

class PagesAdmin(admin.ModelAdmin):
    list_display = ('description', 'filename')
    list_filter = ('description', 'filename')
    search_fields = ['filename']

class ScreensAdmin(admin.ModelAdmin):
    list_display = ('name', 'code_name', 'page')
    list_filter = ('name', 'page')
    search_fields = ['name', 'code_name']

class SurveysAdmin(admin.ModelAdmin):
    list_display = ('subject', 'author', 'date_creation', 'date_end', 'is_shown')
    list_filter = ('subject', 'author', 'date_creation', 'date_end', 'is_shown')
    search_fields = ['subject', 'author', 'date_creation', 'date_end']
    
class InfoTypesAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ['name']

class InformationsAdmin(admin.ModelAdmin):
    list_display = ('type', 'author', 'date_creation', 'date_end', 'is_shown')
    list_filter = ('type', 'author', 'date_creation', 'date_end')
    search_fields = ['type', 'author', 'date_creation', 'date_end']

class MealsAdmin(admin.ModelAdmin):
    list_display = ('is_midday', 'date')
    list_filter = ('is_midday', 'date', 'to_eat')
    search_fields = ['is_midday', 'date', 'to_eat']

class FoodsAdmin(admin.ModelAdmin):
    list_display = ('name', 'meal_part')
    list_filter = ('name', 'meal_part')
    search_fields = ['name', 'meal_part']

class MealPartsAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name', )
    search_fields = ['name']

class TeachersAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ['name']

class AbsentsAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'date_start', 'date_end')
    list_filter = ('teacher', 'date_start', 'date_end')
    search_fields = ['teacher', 'date_start', 'date_end']

class SurveysAdmin(admin.ModelAdmin):
    list_display = ("subject", "author", "date_creation", "date_end", "is_shown")
    list_filter = ('subject', "author", "date_creation", "date_end", "is_shown")
    search_fields = ['subject', 'author', "date_creation", "date_end",]

class AnswersAdmin(admin.ModelAdmin):
    list_display = ("survey", "answer")
    list_filter = ("survey", "answer")
    search_fields = ['survey', "answer"]

class VotesAdmin(admin.ModelAdmin):
    list_display = ("author", "answer", "survey")
    list_filter = ("author", "answer", "survey")
    search_fields = ['author', "answer", "survey"]
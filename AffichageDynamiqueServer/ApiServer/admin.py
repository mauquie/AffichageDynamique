from django.contrib import admin
from .models import * 
from django.contrib.auth.models import Permission

admin.site.register(Permission)
admin.site.register(GroupsExtend)
admin.site.register(Articles, ArticlesAdmin)
admin.site.register(Screens, ScreensAdmin)
admin.site.register(Pages, PagesAdmin)
admin.site.register(Users, UsersAdmin)
admin.site.register(Informations, InformationsAdmin)
admin.site.register(InfoTypes, InfoTypesAdmin)
admin.site.register(Meals, MealsAdmin)
admin.site.register(Foods, FoodsAdmin)
admin.site.register(MealParts, MealPartsAdmin)
admin.site.register(Teachers, TeachersAdmin)
admin.site.register(Absents, AbsentsAdmin)
admin.site.register(Surveys, SurveysAdmin)
admin.site.register(Answers, AnswersAdmin)
admin.site.register(Votes, VotesAdmin)

from django.contrib import admin
from .models import Article, ArticleAdmin, Display, DisplayAdmin, Info, InfoAdmin, InfoType, InfoTypeAdmin, Page, PageAdmin, Survey, SurveyAdmin, User, UserAdmin, GroupExtend
from django.contrib.auth.models import Permission

admin.site.register(Permission)
admin.site.register(GroupExtend)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Display, DisplayAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Survey, SurveyAdmin)
admin.site.register(Info, InfoAdmin)
admin.site.register(InfoType, InfoTypeAdmin)

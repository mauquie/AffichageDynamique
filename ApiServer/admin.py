from django.contrib import admin
from .models import Article, ArticleAdmin, Display, DisplayAdmin, Page, PageAdmin

admin.site.register(Article, ArticleAdmin)
admin.site.register(Display, DisplayAdmin)
admin.site.register(Page, PageAdmin)

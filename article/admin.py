from django.contrib import admin


from .models import ArticlePost, ArticleColumn


# Regiser ArticlePost to admin
admin.site.register(ArticlePost)

# resiter ArticleColumn
admin.site.register(ArticleColumn)
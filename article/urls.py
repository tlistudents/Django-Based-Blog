from django.urls import path
from . import views

app_name = 'article'

urlpatterns = [
    # article list
    path('article-list/', views.article_list, name='article_list'),
    # article detail
    path('article-detail/<int:id>/', views.article_detail, name='article_detail'),
    # write article
    path('article-create/', views.article_create, name='article_create'),
    # delete article
    path('article-delete/<int:id>/', views.article_delete, name='article_delete'),
    # safe delete article
    path('article-safe-delete/<int:id>/', views.article_safe_delete, name='article_safe_delete'),
    # update article
    path('article-update/<int:id>/', views.article_update, name='article_update'),
    # like ++
    path('increase-likes/<int:id>/', views.IncreaseLikesView.as_view(), name='increase_likes'),
    # list view
    path('list-view/', views.ArticleListView.as_view(), name='list_view'),
    # list view detail
    path('detail-view/<int:pk>/', views.ArticleDetailView.as_view(), name='detail_view'),
    # create list view
    path('create-view/', views.ArticleCreateView.as_view(), name='create_view'),
]
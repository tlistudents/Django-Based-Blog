from django.urls import path
# 引入views.py
from . import views

app_name = 'notice'

urlpatterns = [
    # noticce list
    path('list/', views.CommentNoticeListView.as_view(), name='list'),
    path('update/', views.CommentNoticeUpdateView.as_view(), name='update'),
]
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

import notifications.urls

from article.views import article_list
from resume.views import resume_url


urlpatterns = [
    path('admin/', admin.site.urls),
    # home
    path('', resume_url, name='resume'),
    path('blog/', article_list, name='home'),
    path('blog/password-reset/', include('password_reset.urls')),
    path('blog/article/', include('article.urls', namespace='article')),
    path('blog/userprofile/', include('userprofile.urls', namespace='userprofile')),
    path('blog/comment/', include('comment.urls', namespace='comment')),
    # djang-notifications
    path('blog/inbox/notifications/', include(notifications.urls, namespace='notifications')),
    # notice
    path('blog/notice/', include('notice.urls', namespace='notice')),
    # django-allauth
    path('blog/accounts/', include('allauth.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

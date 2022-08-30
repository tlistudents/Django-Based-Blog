from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

import notifications.urls

from article.views import article_list


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', article_list, name='home'),
    path('password-reset/', include('password_reset.urls')),
    path('article/', include('article.urls', namespace='article')),
    path('userprofile/', include('userprofile.urls', namespace='userprofile')),
    path('comment/', include('comment.urls', namespace='comment')),
    path('inbox/notifications/', include(notifications.urls, namespace='notifications')),
    path('notice/', include('notice.urls', namespace='notice')),
    path('accounts/', include('allauth.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

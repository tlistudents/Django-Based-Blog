from django.shortcuts import render, redirect

from django.views import View
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from article.models import ArticlePost


class CommentNoticeListView(LoginRequiredMixin, ListView):
    #notice list
    context_object_name = 'notices'
    # template path
    template_name = 'notice/list.html'
    # redirect
    login_url = '/accounts/login/'
    # unread notice search
    def get_queryset(self):
        return self.request.user.notifications.unread()


class CommentNoticeUpdateView(View):
    """Notice update"""
    # handle GET request
    def get(self, request):
        # update single notice
        notice_id = request.GET.get('notice_id')
        if notice_id:
            article = ArticlePost.objects.get(id=request.GET.get('article_id'))
            request.user.notifications.get(id=notice_id).mark_as_read()
            return redirect(article)
        # update all 
        else:
            request.user.notifications.mark_all_as_read()
            return redirect('notice:list')
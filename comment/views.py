from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse

from .forms import CommentForm
from article.models import ArticlePost
from .models import Comment

from notifications.signals import notify
from django.contrib.auth.models import User


# article comment
@login_required(login_url='/userprofile/login/')
def post_comment(request, article_id, parent_comment_id=None):
    article = get_object_or_404(ArticlePost, id=article_id)

    # handle post request
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.user = request.user

            # secondary reply
            if parent_comment_id:
                parent_comment = Comment.objects.get(id=parent_comment_id)
                # if reply level is over 2, change it to 2
                new_comment.parent_id = parent_comment.get_root().id
                # people being replied
                new_comment.reply_to = parent_comment.user
                new_comment.save()

                # secnd user notive about that he/she is being replied
                if not parent_comment.user.is_superuser and not parent_comment.user == request.user:
                    notify.send(
                        request.user,
                        recipient=parent_comment.user,
                        verb='reply you',
                        target=article,
                        action_object=new_comment,
                    )

                # return HttpResponse("200 OK")
                return JsonResponse({"code": "200 OK", "new_comment_id": new_comment.id})

            new_comment.save()
            
            # send admin notice
            if not request.user.is_superuser:
                notify.send(
                        request.user,
                        recipient=User.objects.filter(is_superuser=1),
                        verb='reply you',
                        target=article,
                        action_object=new_comment,
                    )

            # add Anchor point
            redirect_url = article.get_absolute_url() + '#comment_elem_' + str(new_comment.id)
            return redirect(redirect_url)
        else:
            return HttpResponse("Content invalid, please change the content!")
    # handle get request
    elif request.method == 'GET':
        comment_form = CommentForm()
        context = {
            'comment_form': comment_form,
            'article_id': article_id,
            'parent_comment_id': parent_comment_id
        }
        return render(request, 'comment/reply.html', context)
    # handle other request
    else:
        return HttpResponse("Only GET/POST request is acceptable")

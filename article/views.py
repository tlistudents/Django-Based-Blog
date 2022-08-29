from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import ArticlePost, ArticleColumn
from .forms import ArticlePostForm
import markdown
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from comment.models import Comment

# handle forms
from comment.forms import CommentForm

# handle view
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView

# from my_blog.settings import LOGGING
# import logging
# logging.config.dictConfig(LOGGING)
# logger = logging.getLogger('django.request')


def article_list(request):
    # get infor fron url
    search = request.GET.get('search')
    order = request.GET.get('order')
    column = request.GET.get('column')
    tag = request.GET.get('tag')


    article_list = ArticlePost.objects.all()

    # search article
    if search:
        article_list = article_list.filter(
            Q(title__icontains=search) |
            Q(body__icontains=search)
        )
    else:
        # if not search make it empty
        search = ''

    # colum
    if column is not None and column.isdigit():
        article_list = article_list.filter(column=column)

    # tage
    if tag and tag != 'None':
        article_list = article_list.filter(tags__name__in=[tag])

    # order
    if order == 'total_views':
        # order by number of views
        article_list = article_list.order_by('-total_views')

    # shows 5 article each page
    paginator = Paginator(article_list, 5)
    # get page number from url
    page = request.GET.get('page')
    # get page number to the article
    articles = paginator.get_page(page)
    context = {
        'articles': articles,
        'order': order,
        'search': search,
        'column': column,
        'tag': tag,
    }
    # return context to static page
    return render(request, 'article/list.html', context)


def article_detail(request, id):
    # get the article
    # article = ArticlePost.objects.get(id=id)
    # logger.warning('Something went wrong!')
    article = get_object_or_404(ArticlePost, id=id)
    
    # get commnets
    comments = Comment.objects.filter(article=id)

    # view++
    article.total_views += 1
    article.save(update_fields=['total_views'])

    # neibor article 
    pre_article = ArticlePost.objects.filter(id__lt=article.id).order_by('-id')
    next_article = ArticlePost.objects.filter(id__gt=article.id).order_by('id')
    if pre_article.count() > 0:
        pre_article = pre_article[0]
    else:
        pre_article = None

    if next_article.count() > 0:
        next_article = next_article[0]
    else:
        next_article = None


    # use Markdown editor 
    md = markdown.Markdown(
        extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
        ]
    )
    article.body = md.convert(article.body)

    # forms for comment
    comment_form = CommentForm()

    # get context for the model in static page
    context = { 
        'article': article,
        'toc': md.toc,
        'comments': comments,
        'pre_article': pre_article,
        'next_article': next_article,
        'comment_form': comment_form,
    }
    # return model for the context
    return render(request, 'article/detail.html', context)


# create article(need user to login in order to post article)
@login_required(login_url='/userprofile/login/')
def article_create(request):
    # determine if user post article, if so put the infor into form that
    # meet the data type requirnemnt, and set the author to the login user
    # and save all those to the data base
    if request.method == "POST":
        article_post_form = ArticlePostForm(request.POST, request.FILES)
        if article_post_form.is_valid():
            new_article = article_post_form.save(commit=False)
            new_article.author = User.objects.get(id=request.user.id)
            if request.POST['column'] != 'none':
                new_article.column = ArticleColumn.objects.get(id=request.POST['column'])
            new_article.save()
            # tags is many to many relation
            article_post_form.save_m2m()
            return redirect("article:article_list")
        else:
            return HttpResponse("Content invalid, please change the content!")
    # user request teh data
    else:
        article_post_form = ArticlePostForm()
        columns = ArticleColumn.objects.all()
        context = { 'article_post_form': article_post_form, 'columns': columns }
        return render(request, 'article/create.html', context)


# delete article, vulnerable for csrf attack
@login_required(login_url='/userprofile/login/')
def article_delete(request, id):
    # delete by id
    article = ArticlePost.objects.get(id=id)
    if request.user != article.author:
        return HttpResponse("You do not have permission to modify this post!")
    article.delete()
    return redirect("article:article_list")


# safe delete, this method can prevent csrf attack
@login_required(login_url='/userprofile/login/')
def article_safe_delete(request, id):
    if request.method == 'POST':
        article = ArticlePost.objects.get(id=id)
        if request.user != article.author:
            return HttpResponse("You do not have permission to modify this post!")
        article.delete()
        return redirect("article:article_list")
    else:
        return HttpResponse("Only allow post requests")


# update article
@login_required(login_url='/userprofile/login/')
def article_update(request, id):
    """
    bascally overwrite the views(article title, content, etc.) of the article, 
    and use post method to submit article form again.
    """
    article = ArticlePost.objects.get(id=id)

    if request.user != article.author:
        return HttpResponse("You do not have permission to modify this post!")

    if request.method == "POST":
   
        article_post_form = ArticlePostForm(data=request.POST)
 
        if article_post_form.is_valid():
            article.title = request.POST['title']
            article.body = request.POST['body']
            if request.POST['column'] != 'none':
                article.column = ArticleColumn.objects.get(id=request.POST['column'])
            else:
                article.column = None

            if request.FILES.get('avatar'):
                article.avatar = request.FILES.get('avatar')

            article.tags.set(*request.POST.get('tags').split(','), clear=True)
            article.save()
            return redirect("article:article_detail", id=id)
        else:
            return HttpResponse("Content invalid, please change the content!")
    else:
        article_post_form = ArticlePostForm()
        columns = ArticleColumn.objects.all()
        context = { 
            'article': article, 
            'article_post_form': article_post_form,
            'columns': columns,
            'tags': ','.join([x for x in article.tags.names()]),
        }

        return render(request, 'article/update.html', context)


# update number of views
class IncreaseLikesView(View):
    def post(self, request, *args, **kwargs):
        article = ArticlePost.objects.get(id=kwargs.get('id'))
        article.likes += 1
        article.save()
        return HttpResponse('success')


def article_list_example(request):
    if request.method == 'GET':
        articles = ArticlePost.objects.all()
        context = {'articles': articles}
        return render(request, 'article/list.html', context)


class ContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = 'total_views'
        return context


class ArticleListView(ContextMixin, ListView):
    context_object_name = 'articles'
    template_name = 'article/list.html'

    def get_queryset(self):
        queryset = ArticlePost.objects.filter(title='Python')
        return queryset


class ArticleDetailView(DetailView):
    queryset = ArticlePost.objects.all()
    context_object_name = 'article'
    template_name = 'article/detail.html'
    # get the object(article) to be views and views++
    def get_object(self):
        obj = super(ArticleDetailView, self).get_object()
        obj.total_views += 1
        obj.save(update_fields=['total_views'])
        return obj


class ArticleCreateView(CreateView):
    model = ArticlePost
    fields = '__all__'
    template_name = 'article/create_by_class_view.html'
import os
import pathlib
import random
import sys
from datetime import timedelta

import django
import faker
from django.utils import timezone

# add root to Python's searching path
back = os.path.dirname
BASE_DIR = back(back(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)


if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_blog.settings")
    django.setup()

    from article.models import ArticlePost
    from comment.models import Comment
    from django.contrib.auth.models import User
    #print('clean database')
    #ArticlePost.author.objects.all().delete()
    #ArticlePost.avatar.objects.all().delete()
    #ArticlePost.column.objects.all().delete()
    #ArticlePost.tags.objects.all().delete()
    #ArticlePost.title.objects.all().delete()
    #ArticlePost.body.objects.all().delete()
    #ArticlePost.total_views.objects.all().delete()
    #ArticlePost.likes.objects.all().delete()
    #Comment.objects.all().delete()
    #User.objects.all().delete()
    print('create a blog user')
    user = User.objects.create_superuser('admin', 'admin@hellogithub.com', '112400LTz')

    category_list = ['C++', 'Web Dev', '中文', 'Job', 'HTML', 'Django', 'Python']
    tag_list = ['Block Chain', 'Software', 'django', 'MySQL', 'Spring Boot', 'Java', 'C', 'Python', 'C++', 'tag test']
    a_year_ago = timezone.now() - timedelta(days=365)

    print('create categories and tags')
    #for cate in category_list:
    #    ArticlePost.column.objects.create(name=cate)

    #for tag in tag_list:
    #    ArticlePost.tags.objects.create(name=tag)

    print('create a markdown sample post')
    ArticlePost.objects.create(
        title='Markdown Testing',
        body=pathlib.Path(BASE_DIR).joinpath('scripts', 'md.sample').read_text(encoding='utf-8'),
        column=ArticlePost.column.objects.create(name='MarkdownTest'),
        author=user,
    )

    print('create some faked posts published within the past year')
    fake = faker.Faker()  # English
    #fake = faker.Faker('zh_CN') # Chinese
    for _ in range(100):
        tags = ArticlePost.tags.objects.order_by('?')
        tag1 = tags.first()
        tag2 = tags.last()
        cate = ArticlePost.column.objects.order_by('?').first()
        created_time = fake.date_time_between(start_date='-1y', end_date="now",
                                              tzinfo=timezone.get_current_timezone())
        post = ArticlePost.objects.create(
            title=fake.sentence().rstrip('.'),
            body='\n\n'.join(fake.paragraphs(10)),
            created=created_time,
            column=cate,
            author=user,
        )
        post.tags.add(tag1, tag2)
        post.save()

    print('create some comments')
    for post in ArticlePost.objects.all()[:20]:
        post_created_time = post.created
        delta_in_days = '-' + str((timezone.now() - post_created_time).days) + 'd'
        for _ in range(random.randrange(3, 15)):
            Comment.objects.create(
                name=fake.name(),
                email=fake.email(),
                url=fake.uri(),
                text=fake.paragraph(),
                created_time=fake.date_time_between(
                     start_date=delta_in_days, 
                     end_date="now", 
                     tzinfo=timezone.get_current_timezone()),
                post=post,
            )

    print('done!')
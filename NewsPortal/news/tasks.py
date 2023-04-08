from celery import shared_task
import datetime
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from news.models import Post, Category

@shared_task
def send_notifications(preview,pk,title,subscribers):
    html_content = render_to_string(
        'post_created_email.html',
        {
            'text':preview,
            'link': f'{settings.SITE_URL}/posts{pk}'
        }
    )
    msg = EmailMultiAlternatives(subject=title,
                                 body='',
                                 from_email=settings.DEFAULT_FROM_EMAIL,
                                 to=subscribers)

    msg.attach_alternative(html_content, "text/html")
    msg.send()

@shared_task
def my_job():
    today=datetime.datetime.now()
    last_week= today-datetime.timedelta(days=7)
    posts=Post.objects.filter(time_in__gte=last_week)
    print(f'{posts = }')
    # categories= set(posts.values_list('topics', flat=True))
    categories = set(posts.values_list('topics__topic', flat=True))
    print(f'{categories = }')
    subscribers = set(Category.objects.filter(topic__in=categories).values_list('subscribers__email',flat=True))
    print(f'{subscribers = }')
    html_content = render_to_string(
        'daily_post.html',
        {
            'link':settings.SITE_URL,
            'posts':posts,
        }
    )
    msg = EmailMultiAlternatives(subject='Статьи за неделю',
                                 body='',
                                 from_email=settings.DEFAULT_FROM_EMAIL,
                                 to=subscribers)
    msg.attach_alternative(html_content, "text/html")
    msg.send()


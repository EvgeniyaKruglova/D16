import datetime
import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.mail import mail_managers
from django.core.management.base import BaseCommand
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

from news.models import Post, Category

logger = logging.getLogger(__name__)

#наша задача по выводу текста на экран
def my_job():
    today=datetime.datetime.now()
    last_week= today-datetime.timedelta(days=7)
    posts=Post.objects.filter(time_in__gte=last_week)
    categories= set(posts.values_list('topics', flat=True))
    subscribers = set(Category.objects.filter(topic__in=categories).values_list('subscribers__email',flat=True))
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



@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            #trigger=CronTrigger(second="*/10"),
            trigger=CronTrigger(minute="00", hour="18",month="*",day_of_week="5"),
            id="my_job",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")


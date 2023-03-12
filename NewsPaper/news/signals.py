from django.contrib.auth.models import User
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.core.mail.message import EmailMultiAlternatives
from django.conf import settings
from .models import Post, Category, PostCategory
from .tasks import inform_about_new_post

DEFAULT_FROM_EMAIL = settings.DEFAULT_FROM_EMAIL

@receiver(m2m_changed, sender=PostCategory)
def notify_category_subscribers(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        inform_about_new_post(instance)


@receiver(post_save, sender=User)
def notify_about_signup(sender, instance, **kwargs):
    email_subject = f'{instance.username.title()} was registered at {instance.date_joined.strftime("%b %d %Y %H:%M:%S")}'
    email_html_body = render_to_string(
        template_name='news/you_are_signed_up.html',
        context={
            'name': instance.username,
            "date": instance.date_joined,
        }
    )
    msg = EmailMultiAlternatives(
        subject=email_subject,
        body='',
        from_email=DEFAULT_FROM_EMAIL,
        to=[instance.email, ]
    )
    msg.attach_alternative(email_html_body, 'text/html')
    msg.send()
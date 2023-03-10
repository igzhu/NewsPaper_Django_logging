from  django.template.loader import render_to_string
from django.core.mail.message import EmailMultiAlternatives
from django.conf import settings


DEFAULT_FROM_EMAIL = settings.DEFAULT_FROM_EMAIL
def enlist_subscribers(category):
    usr_emails = []
    for usr in category.subscribers.all():
        usr_emails.append(usr.email)
    return usr_emails

def inform_about_new_post(instance):
    template = 'news/mail_in_category_by_signal.html'
    for category in instance.category.all():
        email_subject= f'New post in category: "{category}"'
        users_mails = enlist_subscribers(category)
        email_html_body = render_to_string(
            template_name=template,
            context={
                'category': category,
                "post": instance,
            }
        )
        msg = EmailMultiAlternatives(
            subject=email_subject,
            body='',
            from_email=DEFAULT_FROM_EMAIL,
            to=users_mails
        )
        msg.attach_alternative(email_html_body, 'text/html')
        msg.send()
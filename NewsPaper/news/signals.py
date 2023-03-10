from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

from .models import Post, Category, PostCategory
from .tasks import inform_about_new_post

@receiver(m2m_changed, sender=PostCategory)
def notify_category_subscribers(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        inform_about_new_post(instance)

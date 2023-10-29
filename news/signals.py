from django.db.models.signals import m2m_changed
from django.dispatch import receiver
import requests

from .models import PostCategory
from .tasks import notify_add_news

@receiver(m2m_changed, sender = PostCategory) #Post.postCategory.through
def notify_subscribers(sender, instance, action, **kwargs):
    if action == 'post_add':
        notify_add_news(instance)
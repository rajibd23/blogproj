from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group

@receiver(post_save, sender=User)
def post_save_user_signal_handler(sender, instance, created, **kwargs):
    if created:
       group = Group.objects.get(name='everyone')
       instance.groups.add(group)
       instance.save()
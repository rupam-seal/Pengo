from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.models import User
from .models import Customer
from django.contrib.auth.models import Group

@receiver(post_save, sender=User)
def CreateUser(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='customer')
        instance.groups.add(group)

        Customer.objects.create(user=instance, name=instance.username, email=instance.email)

        username = instance.username

        print('Profile created for ' + username)

@receiver(post_save, sender=User)
def UpdateUser(sender, instance, created, **kwargs):
    if created == False:
        username = instance.username
        instance.customer.save()
        print('Profile updated for ' + username)
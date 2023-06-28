from django.db import models

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


# Create your models here.
class Dean(models.Model):
    id = models.CharField(max_length=100, blank=True,
                          default='', unique=True, primary_key=True)
    owner = models.ForeignKey(
        'auth.User', related_name='deans', on_delete=models.CASCADE, null=True, blank=True)
    # owner_id = models.ForeignKey(
    #     'auth.User', related_name='id', on_delete=models.CASCADE, null=False)
    name = models.CharField(max_length=100, blank=True, default='')

    class Meta:
        ordering = ['id']


class Student(models.Model):
    id = models.CharField(max_length=100, blank=True,
                          default='', unique=True, primary_key=True)
    owner = models.ForeignKey(
        'auth.User', related_name='students', on_delete=models.CASCADE, null=True, blank=True)
    # owner_id = models.ForeignKey(
    #     'auth.User', related_name='id', on_delete=models.CASCADE, null=False)
    name = models.CharField(max_length=100, blank=True, default='')

    class Meta:
        ordering = ['id']


class Session(models.Model):
    time = models.DateTimeField()
    available = models.BooleanField(default=True)
    dean = models.ForeignKey(Dean, on_delete=models.CASCADE)
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ['time']

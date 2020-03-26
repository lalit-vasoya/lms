from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class User(AbstractUser):
    ''' User Extends with extra fields '''
    contact = models.BigIntegerField()
    email   = models.EmailField(unique = True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.first_name
    
    def get_absolute_url(self):
        return reverse("account:profile", kwargs={"pk": self.pk})
    
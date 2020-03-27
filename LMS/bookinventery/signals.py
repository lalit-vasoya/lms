from django.db.models.signals import post_save
from django.dispatch import receiver
from bookinventery.models import Transaction

@receiver(post_save,sender=Transaction)
def send_email(sender,instance,created, **kwargs):
    if not created:
        print('Yes i call')
    else:
        print('Yes i call by save')
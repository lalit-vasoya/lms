from django.db.models.signals import post_save
from django.dispatch import receiver
from bookinventery.models import Transaction,BookDetail
from django.db.models import F

@receiver(post_save,sender=Transaction)
def send_email(sender,instance,created, **kwargs):
    if not created:
        print('Yes i call')
    else:
        print('Yes i call by save')

@receiver(post_save,sender=BookDetail)
def update_waiting_model(sender,instance,created, **kwargs):

    if not created:
        book = instance
        try:
            quantity = book.quantity
            while book.waiting.waitingtime_set.count() > 0 and quantity>=1:
                #when this book waiting list available
                print('Book Waiting List : ',book.waiting.waitingtime_set.count(),'Book Quanity :',book.quantity)
                user = book.waiting.waitingtime_set.order_by('request_time')[0].user  
                book.waiting.user.remove(user) # remove this student from waiting list
                Transaction.objects.create(book=book,issue_by=user) #creating new request for the student
                BookDetail.objects.filter(id=book.id).update(quantity=F('quantity')-1)
                quantity-=1

        except Exception as ex:
            print(ex)
        print('Book updated')

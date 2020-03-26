from django.db import models
from account.models import User
from django.urls import reverse
from django.utils import timezone

class BookCategories(models.Model):
    ''' Books Categories which type of book and it's description '''
    name        = models.CharField(max_length=64)
    description = models.TextField()

    def __str__(self):
        return self.name

class BookDetail(models.Model):
    ''' Books Details who written the book and How many books we have '''
    title       = models.CharField(max_length=64)
    author      = models.CharField(max_length=64)
    quantity    = models.PositiveIntegerField()
    category    = models.ForeignKey(BookCategories,on_delete=models.CASCADE)


    def __str__(self):
        return self.title

class Transaction(models.Model):
    ''' Books Transaction who issue book,which book are issue,how many time he/she ready the book '''

    STATUS = ((0,'Pending'),(1,'Issue'),(2,'Return'))
    
    book         = models.ForeignKey(BookDetail,on_delete=models.CASCADE)
    issue_by     = models.ForeignKey(User,on_delete=models.CASCADE)
    request_date = models.DateTimeField(default=timezone.now)
    issue_date   = models.DateTimeField(null=True,blank=True)
    return_date  = models.DateTimeField(null=True,blank=True)
    status       = models.PositiveIntegerField(choices=STATUS,default=0)

    def __str__(self):
        return self.book.title

class Waiting(models.Model):
    book    = models.OneToOneField(BookDetail,on_delete=models.CASCADE)
    user    = models.ManyToManyField(User,through='WaitingTime')

    def __str__(self):
        return self.book.title

class WaitingTime(models.Model):
    user            = models.ForeignKey(User,on_delete=models.CASCADE)
    waiting         = models.ForeignKey(Waiting,on_delete=models.CASCADE)
    request_time    = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return  str(self.request_time)
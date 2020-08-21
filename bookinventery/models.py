from django.db import models
from account.models import User
from django.urls import reverse

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
    STATUS = ((0,'Pending'),(1,'Issue'),(2,'Return'))

    ''' Books Transaction who issue book,which book are issue,how many time he/she ready the book '''
    book        = models.ForeignKey(BookDetail,on_delete=models.CASCADE)
    issue_by    = models.ForeignKey(User,on_delete=models.CASCADE)
    issue_date  = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True,blank=True)
    status      = models.PositiveIntegerField(choices=STATUS,default=0)

    def __str__(self):
        return self.book.title

    


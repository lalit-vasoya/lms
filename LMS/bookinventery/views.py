from django.shortcuts import render,get_object_or_404
from django.views import View
from django.views.generic import ListView
from bookinventery import models
from django.http import JsonResponse


class SearchBook(View):
    ''' Render The SearchBook Html '''
    def get(self,request,*args, **kwargs):
        books = models.BookDetail.objects.all()
        return render(request,'bookinventery/searchbook.html',{'books':books})

class Issuebook(View):
    ''' Issue Book By User'''
    def get(self,request,*args, **kwargs):
        id = request.GET.get('id',None)
        if id:
            book = get_object_or_404(models.BookDetail,id=id)

            if book.quantity>0:
                models.Transaction.objects.create(book=book,issue_by=request.user)
                book.quantity-=1
                book.save()
                return JsonResponse(status=200,data={'success':True,'msg':"This Book issue by You"})
            else:
                return JsonResponse(status=203,data={'success':"This Book are not avaliable"})
        else:
            return JsonResponse(status=203,data={'fail':False})
        
class Mybook(ListView):
    ''' Show Issue Book '''
    model         = models.Transaction
    template_name = 'bookinventery/mybook.html'    
    extra_context = {'title':'Issue Book'}

    def get_queryset(self):
        return self.model.objects.filter(issue_by=self.request.user,status__in=[0,1])

class Returnbook(ListView):
    ''' Show Return Book '''
    model         = models.Transaction
    template_name = 'bookinventery/mybook.html'   
    extra_context = {'title':'Return Book'}     

    def get_queryset(self):
        return self.model.objects.filter(issue_by=self.request.user,status=2)
        

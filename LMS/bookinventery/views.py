from django.shortcuts               import render,get_object_or_404
from django.views                   import View
from django.views.generic           import ListView
from bookinventery                  import models
from django.http                    import JsonResponse
from django.utils                   import timezone
from django.db.models               import Count

class SearchBook(View):
    ''' Render The SearchBook Html '''
    def get(self,request,*args, **kwargs):
        books = models.BookDetail.objects.all()
        return render(request,'bookinventery/searchbook.html',{'books':books})

class Requestbook(View):
    ''' Issue Book By User'''
    def get(self,request,*args, **kwargs):
        total_issue_book = models.Transaction.objects.filter(issue_by=request.user,status=1).aggregate(count=Count('issue_by'))['count']
        if total_issue_book<3:
            id = request.GET.get('id',None)
            if id:
                book = get_object_or_404(models.BookDetail,id=id)
                if book.quantity>0:
                    models.Transaction.objects.create(book=book,issue_by=request.user)
                    return JsonResponse(status=200,data={'success':True,'msg':"This Book issue by You"})
                else:
                    return JsonResponse(status=203,data={'success':"This Book are not avaliable"})
            else:
                return JsonResponse(status=203,data={'success':"This book not found in Library"})
        else:
            return JsonResponse(status=203,data={'success':"You have "+str(total_issue_book)+" book so you must return at least one"})
            
class Issuebook(ListView):
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

# Librarian 

class Pendingrequest(View):
    ''' Pending Request For The Issue Book'''
    def get(self,request,*args, **kwargs):
        transaction = models.Transaction.objects.all()
        return render(request,'bookinventery/request.html',{'object_list':transaction})
        
class Changestatus(View):
    ''' Change book pending return or issue status by librarian '''
    def get(self,request,*args, **kwargs):
        id          = request.GET.get('id')
        status      = request.GET.get('status')
        result      = models.Transaction.objects.filter(id=id)
        transaction =result[0]
        book        = result[0].book
        '''  Here status 0 = pending ,1 = issue ,2 = return'''
        if result:
            if transaction.status == 0 and status == '1':
                result        = models.Transaction.objects.filter(id=id).update(status=status,issue_date=timezone.now(),return_date=None)
                book.quantity-=1
                book.save()
            elif transaction.status == 1 and status == '2':
                result        = models.Transaction.objects.filter(id=id).update(status=status,return_date=timezone.now())
                book.quantity+=1
                book.save()
            elif transaction.status == 2 and status == '0':
                result     = models.Transaction.objects.filter(id=id).update(status=status,issue_date=None,return_date=None)        
            else:
                return JsonResponse(status=203,data={'success':False,'msg':'This is invalid operation..!','status':transaction.status})
            return JsonResponse(status=200,data={'success':result,'msg':'Status Change Successfully..!'})                
        else:
            return JsonResponse(status=203,data={'success':False,'msg':'Data not found..!'})
        


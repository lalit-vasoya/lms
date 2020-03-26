from django.shortcuts               import render,get_object_or_404,redirect
from django.views                   import View
from django.views.generic           import ListView
from bookinventery                  import models
from django.http                    import JsonResponse
from django.utils                   import timezone
from django.db.models               import Count,Q,F

class SearchBook(View):
    ''' Render The SearchBook Html '''
    def get(self,request,*args, **kwargs):
        books = models.BookDetail.objects.all()
        return render(request,'bookinventery/searchbook.html',{'books':books})

class Requestbook(View):
    ''' Issue Book By User'''
    def get(self,request,*args, **kwargs):
        total_issue_book = models.Transaction.objects.filter(issue_by=request.user,status=0).aggregate(count=Count('issue_by'))['count']
        if total_issue_book<3:
            id = request.GET.get('id',None)
            if id:
                book = get_object_or_404(models.BookDetail,id=id)
                
                if book.quantity>0:
                    models.Transaction.objects.create(book=book,issue_by=request.user)
                    book.quantity-=1
                    book.save()
                    return JsonResponse(status=200,data={'success':True,'msg':"Request Sent For This Book,Book bring from library"})
                else:
                    if models.Waiting.objects.filter(book=book).exists():
                        print('----------------------------------if')
                        if models.Waiting.objects.filter(~Q(user=request.user)).exists():
                            wait = models.Waiting.objects.get(book=book)
                            wait.user.add(request.user,through_defaults={'request_time':timezone.now()})
                        else:
                            return JsonResponse(status=203,data={'success':"You are already in waiting list..!"})
                    else:
                        print('----------------------------------else')
                        wait = models.Waiting.objects.create(book=book)
                        wait.user.add(request.user,through_defaults={'request_time':timezone.now()})
                    return JsonResponse(status=203,data={'success':"This Book Not Available Yet,So You are add in Waiting List For This book..!"})
            else:
                return JsonResponse(status=203,data={'success':"This book not found in Library..!"})
        else:
            return JsonResponse(status=203,data={'success':"You already  "+str(total_issue_book)+" book request so you must return at least one"})
            
class Issuebook(ListView):
    ''' Show Issue Book '''
    model         = models.Transaction
    template_name = 'bookinventery/mybook.html'    
    extra_context = {'title':'Issue Book'}

    def get_queryset(self):
        if self.request.user.is_staff:
            return self.model.objects.filter(status__in=[0,1])
        else:
            return self.model.objects.filter(issue_by=self.request.user,status__in=[0,1])


class Returnbook(ListView):
    ''' Show Return Book '''
    model         = models.Transaction
    template_name = 'bookinventery/mybook.html'   
    extra_context = {'title':'Return Book'}     

    def get_queryset(self):
        if self.request.user.is_staff:
            return self.model.objects.filter(status=2)
        else:
            return self.model.objects.filter(issue_by=self.request.user,status=2)

# Librarian 

class Pendingrequest(View):
    ''' Pending Request For The Issue Book'''
    def get(self,request,*args, **kwargs):
        transaction = models.Transaction.objects.order_by('status','request_date')
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
                
            elif transaction.status == 1 and status == '2':
                result        = models.Transaction.objects.filter(id=id).update(status=status,return_date=timezone.now())
                # Assaign First Student who in waitin list
                try:
                    if book.waiting.waitingtime_set.count() > 0:
                        user = book.waiting.waitingtime_set.order_by('request_time')[0].user  
                        book.waiting.user.remove(user) # remove this student from waiting list
                        models.Transaction.objects.create(book=book,issue_by=user)
                except:
                        pass
                book.quantity+=1
                book.save()

            else:
                return JsonResponse(status=203,data={'success':False,'msg':'This is invalid operation..!','status':transaction.status})

            return JsonResponse(status=200,data={'success':result,'msg':'Status Change Successfully..!','status':transaction.status})                
        else:
            return JsonResponse(status=203,data={'success':False,'msg':'Data not found..!'})

class Deleterequest(View):
    ''' Delete pending request '''
    def get(self,request,*args, **kwargs):
        # tran = models.Transaction.objects.get(id=kwargs['id'])
        # book = models.BookDetail.objects.filter(id=tran.book.id).update(quantity=F('quantity')-1)        
        return redirect('bookinventery:pendingrequest')

class Waitinglist(View):
    ''' See The Book Waiting List '''
    def get(self,request,*args, **kwargs):
        if request.user.is_staff:
            waiting = (models.Waiting.objects.annotate(usercount=Count('user')).filter(usercount__gt=0))
        else:    
            waiting = models.Waiting.objects.filter(user=request.user)
        return render(request,'bookinventery/waitinglist.html',{'waiting':waiting})

class Waitingqueue(View):
    ''' Geting Queue Of Waiting List '''
    def get(self,request,*args, **kwargs):
        id      = request.GET.get('id',None)
        book    = get_object_or_404(models.BookDetail,id=id)
        waiting = book.waiting.waitingtime_set.order_by('request_time')
        print(waiting)
        student = []
        re_time = []
        for i in waiting:
            student.append(i.user.first_name.capitalize())
            re_time.append(i.request_time.strftime("%b %d %Y %H:%M:%S"))
            
        return JsonResponse(status=200,data={'success':True,'msg':'Data not found..!','student':student,'re_time':re_time})
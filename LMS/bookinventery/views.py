from django.shortcuts               import render,get_object_or_404,redirect,reverse
from django.views                   import View
from django.views.generic           import ListView
from django.contrib                 import messages
from bookinventery                  import models
from django.http                    import JsonResponse
from django.utils                   import timezone
from django.db.models               import Count,Q,F
from django.contrib.auth.decorators import login_required
from django.utils.decorators        import method_decorator
from django.core.mail               import send_mail
from LMS                            import password
from django.core.serializers        import serialize
import threading
from itertools                      import chain

@method_decorator(login_required, name='dispatch')
class Searchbook(View):
    ''' Render The SearchBook Html '''
    def get(self,request,*args, **kwargs):
        books = models.BookDetail.objects.all()
        return render(request,'bookinventery/searchbook.html',{'books':books})

@method_decorator(login_required, name='dispatch')
class Searchbookajax(View):
    ''' Search Book on autosearch '''
    def get(self,request,*args, **kwargs):
        searchtext  = request.GET.get('searchtext',None)
        if searchtext=="":
            books = models.BookDetail.objects.all()
        else:
            books       = models.BookDetail.objects.filter(title__icontains=searchtext)
        context     ={'books':serialize('json',books)}
        context['success']  = True
        return JsonResponse(status=200,data=context)
                

@method_decorator(login_required, name='dispatch')
class Requestbook(View):
    ''' Issue Book By User'''
    def get(self,request,*args, **kwargs):
        total_issue_book = models.Transaction.objects.filter(issue_by=request.user,status=0).aggregate(count=Count('issue_by'))['count']
        if total_issue_book<3:
            id = request.GET.get('id',None)
            if id:
                book = get_object_or_404(models.BookDetail,id=id)
                if models.Transaction.objects.filter(book=book,issue_by=request.user,status__in=[0,1]).count()>0:
                    return JsonResponse(status=200,data={'success':True,'msg':"You sent request already for this Book "})

                if book.quantity>0:
                    models.Transaction.objects.create(book=book,issue_by=request.user)
                    book.quantity-=1
                    book.save()
                    return JsonResponse(status=200,data={'success':True,'msg':"Request Sent For This Book,Book bring from library",'deduce':True})
                       
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
            
@method_decorator(login_required, name='dispatch')
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


@method_decorator(login_required, name='dispatch')
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

@method_decorator(login_required, name='dispatch')
class Pendingrequest(View):
    ''' Pending Request For The Issue Book'''
    def get(self,request,*args, **kwargs):
        transaction = models.Transaction.objects.filter(status__in=[0,1]).order_by('status','request_date')
        return render(request,'bookinventery/request.html',{'object_list':transaction})


        

@method_decorator(login_required, name='dispatch')
class Acceptrequest(View):
    ''' Accept Pending Request and issue the Book Status '''
    def get(self,request,*args, **kwargs):
        id  = kwargs['id']     
        models.Transaction.objects.filter(id=id).update(status=1,issue_date=timezone.now(),return_date=None)  
        x = threading.Thread(target=self.do_mail, args=(id,))
        x.start()
        return redirect('bookinventery:pendingrequest')

    def do_mail(self,id):
        tran = models.Transaction.objects.select_related('book','issue_by').get(id=id)
        student_msg=tran.book.title+" Book issue by You from library at "+str(tran.issue_date)+" Please return as soon as possible..!"        
        res = send_mail('Your Book Issued', student_msg,password.EMAIL, [tran.issue_by.email])  
        print('mail sending success')           

@method_decorator(login_required, name='dispatch')
class Returnrequest(View):
    ''' Return Book Status '''
    def get(self,request,*args, **kwargs):
        id  = kwargs['id']     
        book = get_object_or_404(models.Transaction,id=id).book  
        result        = models.Transaction.objects.filter(id=id).update(status=2,return_date=timezone.now())
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

        return redirect('bookinventery:pendingrequest')

@method_decorator(login_required, name='dispatch')
class Deleterequest(View):
    ''' Delete book pending return by Librarian '''
    def get(self,request,*args, **kwargs):
        id  = kwargs['id']     
        try:
            transaction = get_object_or_404(models.Transaction,id=id)  
            if transaction.status==0:
                book = get_object_or_404(models.BookDetail,id=transaction.book.id)  
                id   = transaction.book.id
                transaction.delete()
                if models.Waiting.objects.filter(book=book).count()==0:
                    #when this book waiting is not available
                    models.BookDetail.objects.filter(id=id).update(quantity=F('quantity')+1)

                if book.waiting.waitingtime_set.count() > 0:
                    #when this book waiting list available
                    user = book.waiting.waitingtime_set.order_by('request_time')[0].user  
                    book.waiting.user.remove(user) # remove this student from waiting list
                    models.Transaction.objects.create(book=book,issue_by=user) #creating new request for the student
                else:
                    print('-----------------else')
                    models.BookDetail.objects.filter(id=id).update(quantity=F('quantity')+1)

        except Exception as e:
            print(e)
        if request.user.is_staff:
            return redirect('bookinventery:pendingrequest')
        return redirect('bookinventery:issuebook')

@method_decorator(login_required, name='dispatch')
class Waitinglist(View):
    ''' See The Book Waiting List '''
    def get(self,request,*args, **kwargs):
        if request.user.is_staff:
            waiting = (models.Waiting.objects.annotate(usercount=Count('user')).filter(usercount__gt=0))
        else:    
            waiting = models.Waiting.objects.filter(user=request.user)
        return render(request,'bookinventery/waitinglist.html',{'waiting':waiting})

    

@method_decorator(login_required, name='dispatch')
class Waitingqueue(View):
    ''' Geting Queue Of Waiting List '''
    def get(self,request,*args, **kwargs):
        id      = request.GET.get('id',None)
        book    = get_object_or_404(models.BookDetail,id=id)
        waiting = book.waiting.waitingtime_set.order_by('request_time')
        student = []
        re_time = []
        delete_url = []
        for i in waiting:
            student.append(i.user.first_name.capitalize())
            re_time.append(i.request_time.strftime("%b %d %Y %H:%M:%S"))
            delete_url.append(reverse('bookinventery:deletepen',kwargs={'id':book.waiting.id}) if i.user == request.user else False)

        return JsonResponse(status=200,
            data={'success':True,
                  'msg':'Data not found..!',
                  'student':student,'re_time':re_time,'url':delete_url
                  })

@method_decorator(login_required, name='dispatch')
class Deletepen(View):

    def get(self,request,*args, **kwargs):
        id      = kwargs.get('id',None)
        book    = get_object_or_404(models.BookDetail,id=id)
        book.waiting.user.remove(request.user)
        return redirect('account:index')
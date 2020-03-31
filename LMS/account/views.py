from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView,DetailView
from django.http import HttpResponse
from django.shortcuts import redirect
from account import forms
from django.contrib import messages
from django.contrib.auth import logout,login,authenticate
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from account import models

@method_decorator(login_required, name='dispatch')
class Index(TemplateView):
    ''' Template View For Index url. it's render '''
    template_name = 'account/index.html'


class Singup(View):

    def get(self,request,*args, **kwargs):
        form = forms.SingupForm()   
        return render(request,'account/signup.html',{'form':form})

    def post(self,request,*args, **kwargs):
        form = forms.SingupForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            messages.success(request,'Register Successfull..!')
            return redirect('account:login')
        else:
            form = forms.SingupForm(request.POST)   
            messages.error(request,'Fill Valid Data!')
            return render(request,'account/signup.html',{'form':form})

class Login(View):
    '''Login the user then render profile page'''

    def get(self,request,*args, **kwargs):
        form  = forms.LoginForm()
        return render(request,'account/login.html',{'form':form})

    def post(self,request,*args, **kwargs):
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            email=form.cleaned_data.get('email')
            password=form.cleaned_data.get('password')
            user = authenticate(email=email,password=password)
            if user:
                login(request,user)
                messages.success(request,'Login Successfull..!')
                return redirect('account:index')    
            else:
                messages.error(request,'Fill Valid Data..!')
                return render(request,'account/login.html',{'form':form})            
        else:
            form  = forms.LoginForm()
            messages.error(request,'Fill Valid Data..!')
            return render(request,'account/login.html',{'form':form})            


class Logout(View):
    '''Logout the user then render index page'''

    def get(self,request,*args, **kwargs):
        logout(request)    
        return redirect('account:login')    

class Profile(DetailView):
    model         = models.User
    template_name = 'account/profile.html'

@method_decorator(login_required, name='dispatch')
class Updateprofile(View):

    def get(self,request,*args, **kwargs):
        form = forms.ProfileUpdateForm()
        return render(request,'account/updateprofile.html',{'form':form})           

    def post(self,request,*args, **kwargs):
        form = forms.ProfileUpdateForm(request.POST,instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = request.user.email
            user.save()
            return redirect('account:profile',pk=request.user.id)
        return render(request,'account/updateprofile.html',{'form':form})           
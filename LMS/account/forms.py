from django import forms
from account import models
from django.contrib.auth.forms import UserCreationForm

class SingupForm(UserCreationForm):
    class Meta:
        model  = models.User
        fields = ['first_name','last_name','contact','email','username','password1','password2']

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class':'form-control','placeholder':self.fields[field].label})

class LoginForm(forms.Form): 
    email   = forms.CharField(max_length=40,label="Enter Email",widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter Email'}))
    password  = forms.CharField(max_length=20,label="Enter Password",widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter Password'}))
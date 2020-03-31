from django.urls import path
from account import views

app_name = 'account'
urlpatterns = [
    path('',views.Index.as_view(),name='index'),
    path('login',views.Login.as_view(),name='login'),
    path('singup',views.Singup.as_view(),name='singup'),
    path('logout',views.Logout.as_view(),name='logout'),
    path('updateprofile',views.Updateprofile.as_view(),name='updateprofile'),
    path('<int:pk>/profile',views.Profile.as_view(),name='profile'),
]

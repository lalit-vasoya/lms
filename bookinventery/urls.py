from django.urls import path
from bookinventery import views

app_name='bookinventery'
urlpatterns = [
    path('searchbook',views.SearchBook.as_view(),name='searchbook'),   
    path('issuebook',views.Issuebook.as_view(),name='issuebook'),
    path('returnbook',views.Returnbook.as_view(),name='returnbook'),
    path('mybook',views.Mybook.as_view(),name='mybook')
]

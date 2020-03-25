from django.urls import path
from bookinventery import views

app_name='bookinventery'
urlpatterns = [
    #student profile url
    path('searchbook',views.SearchBook.as_view(),name='searchbook'),   
    path('requestbook',views.Requestbook.as_view(),name='requestbook'),
    path('issuebook',views.Issuebook.as_view(),name='issuebook'),
    path('returnbook',views.Returnbook.as_view(),name='returnbook'),

    #librarian profile url
    path('pendingrequest',views.Pendingrequest.as_view(),name='pendingrequest'),
    path('changestatus',views.Changestatus.as_view(),name='changestatus'),
]

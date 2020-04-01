from django.urls import path
from bookinventery import views

app_name='bookinventery'
urlpatterns = [
    #student profile url
    path('searchbook',views.Searchbook.as_view(),name='searchbook'),   
    path('searchbookajax',views.Searchbookajax.as_view(),name='searchbookajax'),
    path('requestbook',views.Requestbook.as_view(),name='requestbook'),
    path('issuebook',views.Issuebook.as_view(),name='issuebook'),
    path('returnbook',views.Returnbook.as_view(),name='returnbook'),
    path('waitinglist',views.Waitinglist.as_view(),name='waitinglist'),
    path('waitingqueue',views.Waitingqueue.as_view(),name='waitingqueue'),
    path('<int:id>/deletepen',views.Deletepen.as_view(),name='deletepen'),

    #librarian profile url
    path('pendingrequest',views.Pendingrequest.as_view(),name='pendingrequest'),
    path('<int:id>/acceptrequest',views.Acceptrequest.as_view(),name='acceptrequest'),
    path('<int:id>/returnrequest',views.Returnrequest.as_view(),name='returnrequest'),
    path('<int:id>/deleterequest',views.Deleterequest.as_view(),name='deleterequest'),
]

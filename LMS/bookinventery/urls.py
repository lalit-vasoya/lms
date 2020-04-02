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
    #books
    path('listbook',views.Listbook.as_view(),name='listbook'),
    path('createbook',views.Createbook.as_view(),name='createbook'),
    path('<int:id>/updatebook',views.Updatebook.as_view(),name='updatebook'),
    path('<int:id>/deletebook',views.Deletebook.as_view(),name='deletebook'),
    #books categories
    path('listbookcategory',views.Listbookcategory.as_view(),name='listbookcategory'),
    path('createbookcategory',views.Createbookcategory.as_view(),name='createbookcategory'),
    path('<int:id>/updatebookcategory',views.Updatebookcategory.as_view(),name='updatebookcategory'),
    path('<int:id>/deletebookcategory',views.Deletebookcategory.as_view(),name='deletebookcategory'),
]

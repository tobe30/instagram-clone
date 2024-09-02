from django.urls import path
from directs import views 

urlpatterns = [
    path('inbox/', views.inbox, name="inbox"),
    path('directs/<username>', views.direct, name="directs"),
    path('send/', views.SendMessage, name="send-message"),
    path('new/', views.UserSearch, name="user-search"),
    path('new/<username>', views.NewMessage, name="new-message"),




   

]
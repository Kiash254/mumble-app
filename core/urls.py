from django.urls import path

from .views import home,room,CreateView,UpdateView,DeleteView,LoginPage,LogoutPage,RegisterPage,Deletemessage

app_name='core'

urlpatterns = [
    path('login/',LoginPage,name='login'),
    path('logout/',LogoutPage,name='logout'),
    path('register/',RegisterPage,name='register'),
    path('', home, name='home'),
    path('room/<int:pk>/',room,name='room'),
    path('create-room/',CreateView,name='create-room'),
    path('update-room/<int:pk>/',UpdateView,name='update-room'),
    path('delete-room/<int:pk>/',DeleteView,name='delete-room'),
    path('delete-message/<int:pk>/',Deletemessage,name='delete-message'),
]
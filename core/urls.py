from django.urls import path

from .views import home,room,CreateView,UpdateView,DeleteView

app_name='core'

urlpatterns = [
    path('', home, name='home'),
    path('room/<int:pk>/',room,name='room'),
    path('create-room/',CreateView,name='create-room'),
    path('update-room/<int:pk>/',UpdateView,name='update-room'),
    path('delete-room/<int:pk>/',DeleteView,name='delete-room'),
]
from django.urls import path

from .views import home,room

app_name='core'

urlpatterns = [
    path('', home, name='home'),
    path('room/<int:pk>/',room,name='room')
]
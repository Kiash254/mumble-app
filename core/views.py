from django.shortcuts import render,redirect
from .models import Room,Message,Topic
from .forms import RoomForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout

# Create your views here.


def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request,'Username is not found')
        user=authenticate(request, username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('core:home')
        else:
            messages.error(request,'Invalid username or password')

    context={}
    return render(request,'core/login_register.html',context)

def LogoutPage(request):
    logout(request)
    return redirect('core:login')

def home(request):
    q=request.GET.get('q') if request.GET.get('q') else ''
    
    rooms=Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    
    ) 
    topics=Topic.objects.all()
    room_count=rooms.count()
    context={
        'rooms':rooms,
        'topics':topics,
        'room_count':room_count,
    }
    return render(request,'core/home.html',context)

def room(request,pk):
   
    room=Room.objects.get(id=pk)
    context={
        'room':room,    
    }

    return render(request, 'core/room.html',context)
#CRUD

def CreateView(request):
    form=RoomForm()
    if request.method=='POST':
        form=RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('core:home')
    context={
        'form':form
    }
    return render(request,'core/room_form.html',context)


def UpdateView(request,pk):
    room=Room.objects.get(id=pk)
    form=RoomForm(instance=room)
    if request.method=='POST':
        form=RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('core:home')
    context={
        'form':form
    }
    return render(request,'core/room_form.html',context)

def DeleteView(request,pk):
    room=Room.objects.get(id=pk)
    if request.method=='POST':
        room.delete()
        return redirect('core:home')
    context={
        'room':room
    }
    return render(request,'core/delete.html',context)
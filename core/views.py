from django.shortcuts import render,redirect
from .models import Room,Message,Topic,User
from .forms import RoomForm,Userform,MyUserCreationForm
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
# Create your views here.


def LoginPage(request):
    page='login'
    if request.user.is_authenticated:
        return redirect('core:home')    
    if request.method=='POST':
        email=request.POST.get('email').lower()
        password=request.POST.get('password')
        try:
            user=User.objects.get(email=email)
        except:
            messages.error(request,'Email is not found')
        user=authenticate(request, email=email,password=password)

        if user is not None:
            login(request,user)
            return redirect('core:home')
        else:
            messages.error(request,'Invalid username or password')

    context={
        'page':page,
    }
    return render(request,'core/login_register.html',context)

def LogoutPage(request):
    logout(request)
    return redirect('core:home')

def RegisterPage(request):
    page='register'
    form=MyUserCreationForm()
    if request.method=='POST':
        form=MyUserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            login(request,user)
            return redirect('core:home')
        else:
            messages.error(request,'an error Occoured during registration')
    context={
        'form':form,
    }
    return render(request,'core/login_register.html',context)

def home(request):
    q=request.GET.get('q') if request.GET.get('q') else ''
    rooms=Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    
    ) 
    topics=Topic.objects.all()[0:5]
    room_count=rooms.count()
    room_message=Message.objects.filter(Q(room__topic__name__icontains=q)) 
    context={
        'rooms':rooms,
        'topics':topics,
        'room_count':room_count,
        'room_message':room_message,
    }
    return render(request,'core/home.html',context)

def room(request,pk):
   
    room=Room.objects.get(id=pk)
    room_message=room.message_set.all()
    participants=room.participants.all()
    if request.method=='POST':
        message=Message.objects.create(
            user=request.user,
            room=room,
            content=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('core:room',pk=room.id)
    context={
        'room':room,
        'room_message':room_message,
        'participants':participants,
                   
    }

    return render(request, 'core/room.html',context)

def Profile(request , pk):
    user=User.objects.get(id=pk)
    rooms=user.room_set.all()
    room_message=user.message_set.all()
    topics=Topic.objects.all()
    context={
        'user':user,
        'rooms':rooms,
        'room_message':room_message,
        'topics':topics,
    }
    return render(request,'core/profile.html', context)
#CRUD
@login_required(login_url='core:login')
def CreateView(request):
    form=RoomForm()
    topics=Topic.objects.all()
    if request.method=='POST':
        topic_name=request.POST.get('topic')
        topic,created=Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('core:home')
    context={
        'form':form,
        'topics':topics,
    }
    return render(request,'core/room_form.html',context)

@login_required(login_url='core:login')
def UpdateView(request,pk):
    room=Room.objects.get(id=pk)
    form=RoomForm(instance=room)
    topics=Topic.objects.all()
    if request.user != room.host:
        return HttpResponse('You are not allowed to update this room')
    if request.method=='POST':
        topic_name=request.POST.get('topic')
        topic,created=Topic.objects.get_or_create(name=topic_name)
        room.topic=topic
        room.name=request.POST.get('name')
        room.description=request.POST.get('description')
        room.save()
        return redirect('core:home')
    context={
        'form':form,
        'topics':topics,
        'room':room,
    }
    return render(request,'core/room_form.html',context)
@login_required(login_url='core:login')
def DeleteView(request,pk):
    room=Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('You are not allowed to delete this room')
    if request.method=='POST':
        room.delete()
        return redirect('core:home')
    context={
        'room':room
    }
    return render(request,'core/delete.html',context)

@login_required(login_url='core:login')
def Deletemessage(request,pk):
    message=Message.objects.get(id=pk)
    if request.user != message.host:
        return HttpResponse('You are not allowed to delete this room')
    if request.method=='POST':
        message.delete()
        return redirect('core:home')
    context={
        'message':message
    }
    return render(request,'core/delete.html',context)

@login_required(login_url='core:login')
def UpdateUser(request):
    user=request.user
    form=Userform(instance=user)
    if request.method=='POST':
        form=Userform(request.POST,request.FILES,instance=user)
        if form.is_valid():
            form.save()
            return redirect('core:profile',pk=user.id)
    context={
        'form':form,
    }
    return render(request,'core/update-user.html',context)

def TopicPage(request):
    q=request.GET.get('q') if request.GET.get('q') else ''
    topics=Topic.objects.filter(name__icontains=q)
    context={
        'topics':topics,
    }

    return render(request,'core/topics.html',context)

def ActivityPage(request):
    room_messages=Message.objects.all()
    context={
        'room_messages':room_messages,
    }
    return render(request,'core/activity.html',context)
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import Message, Room, Topic,User
from .forms import RoomForm, UserForm, MyUserCreationForm, TopicForm
# Create your views here.
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver    

@receiver(user_logged_in)
def got_online(sender, user, request, **kwargs):    
    user.is_online = True
    user.save()

@receiver(user_logged_out)
def got_offline(sender, user, request, **kwargs):   
    user.is_online = False
    user.save()

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        # make sure user is exit
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, "ユーザーが存在しません！")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "ユーザー名前またはパスワードが存在しません！")
    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):

    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration!')

    return render(request, 'base/login_register.html', {'form': form})


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    room_count = rooms.count()
    topics = Topic.objects.all()
    topics_first_five = topics[0:5]
    room_messages = Message.objects.filter(
        Q(room__topic__name__icontains=q)
    )
       #reset all the is_active field
    topics.update(is_active=False)
    if q != '':
        topic = Topic.objects.get(name=q)
        topic.is_active = True
        topic.save()
        # pass 

    context = {'rooms': rooms, 'topics': topics_first_five,
               'room_count': room_count,
               'room_messages': room_messages}
               
    return render(request, 'base/home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room': room, 'room_messages': room_messages,
               'participants': participants}
    return render(request, 'base/room.html', context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user,
               'rooms': rooms,
               'room_messages': room_messages,
               'topics': topics}
    return render(request, 'base/profile.html', context)


@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')
    context = {'form': form,
               "topics": topics}
    return render(request, 'base/room_form.html', context)


def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        form = RoomForm(request.POST, instance=room)
        room.name = request.POST.get('name')
        room.topic = topic
        room.name = request.POST.get('name')
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
    context = {'form': form,
               'topics': topics,
               'room': room}
    return render(request, 'base/room_form.html', context)

def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})

def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('you are not allowed here!!')

    if request.method == 'POST':
        message.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj': message})


@login_required(login_url="login")
def updateUser(request):
    form = UserForm(instance=request.user)

    if request.method == "POST":
        form = UserForm(request.POST, request.FILES,instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=request.user.id)

    context = {"form": form}
    return render(request, 'base/update-user.html', context)


def topicsPage(request):

    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    # topics.is_active=True
    # topics.save()
    # .update(is_active=True)
    #
 
#  Client.objects.filter(pk=pk).update(status='active')


    # make sure user is exit
    # try:
    #     topic = Topic.objects.get(id=q)
    #     topic.is_active = True
    #     topic.save()
    # except:
    #     messages.error(request, "")

  

    # form = TopicForm(instance=topic)
    


    # if request.method == 'POST':
        # form = TopicForm(request.POST, instance=topic)

        # topic.is_active = True
        # topic.save()
          # topic.is_active = True
    # if form.is_valid():
    #    topic.save()
    # 
    # topic.save()
  
  

    return render(request, 'base/topics.html', {'topics': topics})


def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'base/activity.html', {'room_messages': room_messages})

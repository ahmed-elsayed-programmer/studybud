from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate , login , logout
from django.contrib import messages


from .models import Massage, Room  , Topic , User 
from .forms import MyUserCreationForm, RoomForm , UserForm

# Create your views here.

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try :
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not ex ${username} ${password}')

        user = authenticate(request , email= email , password= password)

        if user is not  None:
            login(request, user)
            return redirect('home')
        else :
            messages.error(request, "password does not exit "+ email + password)
    
    context = {'page' : page}
    return render(request , 'base/login.html',context)

def logoutUser(requset):
    logout(requset)
    return redirect('home')

def registerUser(request):
    page = 'register'
    form = MyUserCreationForm()
    if request.method =='POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid() :
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user )
            return redirect('home')
        else :
            messages.error(request, 'An error occurd registertion')
    context = {'page': page , 'form': form }
    return render(request , 'base/login.html',context)

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains = q)|
        Q(name__icontains = q)|
        Q(discription__icontains = q)
        )
    topics = Topic.objects.all()
    room_count = rooms.count()
    room_messages = Massage.objects.filter(Q(room__topic__name__contains=q ))

    context = {'rooms' : rooms , 'topics' : topics , 'room_count' :room_count , 'room_messages':room_messages}
    return render(request, 'base/home.html' , context)


def room(request , pk):
    room = Room.objects.get(pk=pk)
    room_message =  room.massage_set.all().order_by('-created')
    participants = room.participants.all()
    if request.method == "POST":
        message= Massage.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk= room.id )
    context = {'room' : room  , 'room_messages': room_message , "participants":participants}
    return render(request, 'base/room.html' , context)


def userProfile(request , pk):
    user = User.objects.get(id =pk )
    rooms = user.room_set.all()
    room_messages = user.massage_set.all()
    topics = Topic.objects.all()
    context =  {'profile' : user , 'rooms' : rooms , 'room_messages' : room_messages,
    'topics' : topics 
    }
    return render(request , 'base/profile.html' ,context)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm( )
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid() :
            room = form.save(commit=False)
            room.host = request.user 
            room.save()
            return redirect('home')

    context = {'form' : form }
    return render(request , 'base/room_form.html' , context)


@login_required(login_url='login')
def updateRoom(request , pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host :
        return HttpResponse('Your  are not allowed here ')

    if request.method == "POST":
        form = RoomForm(request.POST , instance=room)
        if form.is_valid() :
            form.save()
            return redirect('home')

    context = {'form' : form }
    return render(request , 'base/room_form.html' , context)


@login_required(login_url='login')
def deleteRoom(requset,pk):
    room = Room.objects.get(id=pk)
    if requset.method == "POST":
        room.delete()
        return redirect('home')
    return render(requset , 'base/delete.html' , {'obj':room})


@login_required(login_url='login')
def deleteMessage(requset,pk):
    message = Massage.objects.get(id=pk)
    if requset.method == "POST":
        message.delete()
        return redirect('home')
    return render(requset , 'base/delete.html' , {'obj':message})


@login_required(login_url='login')
def updateUser(requset):
    user = requset.user
    form = UserForm(instance= user )
    if requset.method == "POST":
        form = UserForm(requset.POST , requset.FILES , instance= user)
        if form.is_valid() :
            form.save()
            return redirect('user-profile' , pk = user.id )

    context = {'form' :form }
    return render(requset , 'base/update-user.html' , context)
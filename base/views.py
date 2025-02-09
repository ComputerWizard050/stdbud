from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from .models import Chatmessage, Room, Topic, Message, User, Hascontactwith
from .forms import RoomForm, UserForm, MyUserCreationForm, MessageForm
from django.utils.html import format_html
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View


# Create your views 

# rooms = [
#     {'id': 1, 'name': 'Lets learn python!'},
#     {'id': 2, 'name': 'Design with me'},
#     {'id': 3, 'name': 'Frontend developers'},
# ]


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exit')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            login(request, user)
            Hascontactwith.objects.create(user=user)
            return redirect('home')

        else:
            messages.error(request, 'An error occurred during registration')

    return render(request, 'base/login_register.html', {'form': form})


@login_required(login_url='login')
def follow(request):
    all_rooms = Room.objects.all()
    follows_room = []
    for room in all_rooms:
        followers = room.participants.all()
        follows_room.append(followers)
    context = {'all_rooms': all_rooms, 'follows_room': follows_room}
    return render(request, 'base/follow.html', context)


@login_required(login_url='login')
def chats(request):
    table, created = Hascontactwith.objects.get_or_create(user=request.user)
    friends = table.contactpersons.all()

    context = {'friends': friends}

    return render(request, 'base/chats1.html', context)


def home(request):
    if request.user.is_authenticated and request.user.avatar == 'avatar.svg':
        messages.info(request, format_html(
            "<a> href=/update-user/{}</a>", "You don't have profile image yet"))

    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )[0:3]

    # search for users
    users = User.objects.filter(
        Q(username__icontains=q) |
        Q(name__icontains=q) |
        Q(bio__icontains=q) |
        Q(email__icontains=q)
    )[0:5]
    # stop search for users

    # search for message
    messages_found = Message.objects.filter(
        Q(body__icontains=q)
    )[0:5]
    # stop search for message

    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(
        Q(room__topic__name__icontains=q))[0:3]

    user = request.user

    context = {'user': user, 'rooms': rooms, 'topics': topics, 'room_count': room_count,
               'room_messages': room_messages, 'users': users, 'messages_found': messages_found}

    return render(request, 'base/home.html', context)


@login_required(login_url='login')
def chat(request, pk):
    touser = User.objects.get(id=pk)
    fromuser = User.objects.get(id=request.user.id)
    allchats = Chatmessage.objects.filter(Q(touser=touser) & Q(
        fromuser=fromuser) | Q(fromuser=touser) & Q(touser=fromuser))
    add = Hascontactwith.objects.get(user=fromuser)

    if request.method == 'POST':
        if len(request.FILES) != 0:
            uploadfile = request.FILES['image']
            if str(uploadfile).lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                isimg = True

            elif str(uploadfile).lower().endswith(('.mp4')):
                isimg = False
            else:
                isimg = None
                uploadfile = None
        else:
            uploadfile = None
            isimg = None
        print(isimg)

        body = request.POST.get('body')
        if body == '' and uploadfile == None:
            messages.error(request, 'invalid message!')
            return redirect('chat', pk=pk)
        else:
            chatmessage = Chatmessage.objects.create(
                fromuser=request.user,
                touser=touser,
                body=body,
                isimg=isimg,
                uploadfile=uploadfile,
            )
            add.contactpersons.add(touser)
            return redirect('chat', pk=touser.id)

    context = {'touser': touser, 'fromuser': fromuser, 'allchats': allchats}
    return render(request, 'base/chat.html', context)


def room(request, pk):  # hier verder met #19
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()
    notallowed = room.notallowed.all()
    cohosts = room.cohosts.all()
    form = MessageForm()
    # liked = Message.likes.filter(id=request.user.id).exists()

    if request.method == 'POST' and not request.user in notallowed:
        if len(request.FILES) != 0:
            uploadfile = request.FILES['image']
            if str(uploadfile).lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                isimg = True

            elif str(uploadfile).lower().endswith(('.mp4')):
                isimg = False
            else:
                isimg = None
                uploadfile = None
        else:
            uploadfile = None
            isimg = None
        print(isimg)

        body = request.POST.get('body')
        if body == '' and uploadfile == None:
            messages.error(request, 'invalid message!')
            return redirect('room', pk=room.id)
        else:
            message = Message.objects.create(
                user=request.user,
                room=room,
                body=body,
                isimg=isimg,
                uploadfile=uploadfile,
            )
            room.participants.add(request.user)
            return redirect('room', pk=room.id)

    context = {'room': room, 'room_messages': room_messages,
               'participants': participants, 'form': form, 'notallowed': notallowed, 'cohosts': cohosts}
    return render(request, 'base/room.html', context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    # Use get_or_create() to ensure a Hascontactwith instance exists
    usercontacts, created = Hascontactwith.objects.get_or_create(user=request.user)
    topics = Topic.objects.all()
    context = {
        'user': user,
        'rooms': rooms,
        'room_messages': room_messages,
        'topics': topics,
        'usercontacts': usercontacts,
    }
    return render(request, 'base/profile.html', context)


@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    all_rooms = Room.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        if len(request.FILES) != 0:
            doc = request.FILES
            avatar = doc['roomavatar']
        else:
            avatar = 'avatar.svg'
        # deleteProfImg = request.POST.get('delete')
        if request.POST.get('delete') == 'delete':
            avatar = 'avatar.svg'
        roomname = request.POST.get('name')
        for room in all_rooms:
            if room.name == roomname:
                messages.error(
                    request, 'This Roomname Is Already In Use')
                return redirect('create-room')
        # if roomname
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=roomname,  # request.POST.get('name'),
            description=request.POST.get('description'),
            avatar=avatar
        )
        return redirect('user-profile', request.user.id)

    context = {'form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def deleteFollower(request, pku, pkr):
    deleteduser = User.objects.get(id=pku)
    room = Room.objects.get(id=pkr)
    all_cohosts = list(room.cohosts.all())

    if request.user in all_cohosts or request.user == room.host:
        room.notallowed.add(deleteduser)
        room.participants.remove(deleteduser)
    else:
        messages.error(request, 'you are not allowed to do that!')

    return redirect('room', room.id)


@login_required(login_url='login')
def addHost(request, pku, pkr):
    newhost = User.objects.get(id=pku)
    room = Room.objects.get(id=pkr)
    if request.user == room.host:
        room.cohosts.add(newhost)
    else:
        messages.error(request, 'you are not allowed to do that!')
    return redirect('room', room.id)


@login_required(login_url='login')
def unHost(request, pku, pkr):
    host = User.objects.get(id=pku)
    room = Room.objects.get(id=pkr)
    if request.user == room.host:
        room.cohosts.remove(host)
    else:
        messages.error(request, 'you are not allowed to do that!')
    return redirect('room', room.id)


@login_required(login_url='login')
def addFollower(request, pku, pkr):
    addeduser = User.objects.get(id=pku)
    room = Room.objects.get(id=pkr)
    all_cohosts = list(room.cohosts.all())

    if request.user == room.host or request.user in all_cohosts:
        room.notallowed.remove(addeduser)
        room.participants.add(addeduser)
    else:
        messages.error(request, 'you are not allowed to do that!')
    return redirect('room', room.id)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})


@login_required(login_url='login')
def deleteChatMessage(request, pk):
    chat = Chatmessage.objects.get(id=pk)
    if request.user != chat.fromuser:
        return HttpResponse('You are not allowed here!!')

    if request.method == 'POST':
        chat.delete()
        return redirect('chat', chat.touser.id)
    return render(request, 'base/delete.html', {'obj': chat})


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You are not allowed here!!')

    if request.method == 'POST':
        message.delete()
        return redirect('room', message.room.id)
    return render(request, 'base/delete.html', {'obj': message})


@login_required(login_url='login')
def unfollowRoom(request, pku, pkr):
    deleteduser = User.objects.get(id=pku)
    room = Room.objects.get(id=pkr)
    if request.user == room.host:
        messages.error(request, 'you are not allowed to do that!')
    else:
        # room.notallowed.add(deleteduser)
        room.participants.remove(deleteduser)

    return redirect('follow')


def about(request):
    return render(request, 'base/about.html')


@login_required(login_url='login')
def updateUser(request):
    user = request.user  # email of user
    print(user)
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            deleteProfImg = request.POST.get('delete')
            if deleteProfImg == 'delete':
                user.avatar = 'avatar.svg'
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, 'base/update-user.html', {'form': form})


@login_required(login_url='login')
def updateRoomNew(request, pk):
    room = Room.objects.get(id=pk)  # name of room
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.method == 'POST':
        print(request.POST.get('topic'))
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            # deleteProfImg = request.POST.get('delete')
            # if deleteProfImg == 'delete':
            #     room.avatar = 'avatar.svg'
            form.save()
            return redirect('room', pk=room.id)
        else:
            return HttpResponse('wrong')
    context = {'form': form, 'room': room, 'topics': topics}
    return render(request, 'base/room_form_new.html', context)


@login_required(login_url='login')
def updateRoom(request, pk):
    user = request.user
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    all_participants = room.participants.all()
    all_notallowed = room.notallowed.all()
    all_cohosts = list(room.cohosts.all())
    set1 = list(all_notallowed) + list(all_participants)
    total = [i for i in set1 if i not in all_cohosts]
    all_rooms = Room.objects.all()

    if (request.user == room.host) or (request.user in all_cohosts and request.user in all_participants):
        if request.method == 'POST':
            topic_name = request.POST.get('topic')
            topic, created = Topic.objects.get_or_create(name=topic_name)
            room.name = request.POST.get('name')
            for xroom in all_rooms:
                if xroom.name == room.name and xroom.id != room.id:
                    messages.error(request, 'This Roomname Is Already In Use')
                    return redirect('update-room', room.id)

            room.topic = topic
            if len(request.FILES) != 0:
                doc = request.FILES
                room.avatar = doc['roomavatar']
                print(room.avatar)

            deleteProfImg = request.POST.get('delete')
            arrhost = request.POST.getlist('newhost')
            print(arrhost)
            for newhost in arrhost:
                room.cohosts.add(newhost)

            if deleteProfImg == 'delete':
                room.avatar = 'avatar.svg'
            room.description = request.POST.get('description')
            # room.avatar = request.POST.get('avatar')
            # if room.avatar == None:
            #     room.avatar='avatar.svg'
            room.save()
            return redirect('room', room.id)
        context = {'form': form, 'topics': topics, 'user': user, 'cohosts': all_cohosts,
                   'total': total, 'room': room, 'all_participants': all_participants}
        return render(request, 'base/room_form.html', context)
    else:
        return HttpResponse('You are not allowed here!!')


def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {'topics': topics})


def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'base/activity.html', {'room_messages': room_messages})


def contact(request):
    if request.method == "POST":
        message_name = request.POST.get('message_name')
        if request.user.is_authenticated:
            message_email = request.user.email
        else:
            message_email = request.POST.get('message_email')

        message = request.POST.get('message')

        if message_name == None or message_email == None or message == None:
            return redirect('home')
        # mail to helpdesk
        send_mail(
            message_name,
            message +
            ' (from ' + message_email + ')',
            message_email,
            ['delnoyesteftest@gmail.com'],
        )
        # mail to user
        send_mail(
            "You have sent an email to Stef Industries.",
            "your subject was '" + message_name + "'" +
            " your message was: " +
            "'" + message + "'",
            message_email,
            [message_email],
        )
        context = {'message_name': message_name, 'message': message}
        return render(request, 'base/contact.html', context)
    else:
        return render(request, 'base/contact.html')


def forgot_password(request):
    if request.method == "POST":
        subject = 'create new password'
        message = 'create a new password here'
        email_from = 'delnoyesteftest@gmail.com'
        gets_email = request.POST.get('email')

        send_mail(
            subject,
            message,
            email_from,
            [gets_email],
        )
        messages.success(request, 'an email is sent to ' + gets_email+'!!')
        # return redirect('home')
        # context = {'gets_email': gets_email}

        return render(request, 'base/home.html')
    else:
        return render(request, 'base/forgot_password.html')

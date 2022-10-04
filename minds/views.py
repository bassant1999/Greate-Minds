from asyncio.windows_events import NULL
from turtle import title
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password


def index(request):
    stories =""
    readlists = []
    notificationsNum = 0
    chatsNum = 0
    if request.user.is_authenticated:
        stories = Story.objects.filter(writer = request.user)
        readlists = ReadList.objects.filter(reader = request.user)
        notificationsNum = len(Notification.objects.filter(owner=request.user, look=0))
        chatsNum = len(Message.objects.filter(reciever=request.user, look=0))
    stories_list = Story.objects.all().order_by('-created_at')
    paginator = Paginator(stories_list, 10)
    page = request.GET.get('page')
    try:
        storiesList = paginator.page(page)
    except PageNotAnInteger:
        storiesList = paginator.page(1)
    except EmptyPage:
        storiesList = paginator.page(paginator.num_pages)
    return render(request, "minds/index.html", 
    {"stories":stories, "storiesList":storiesList, "readlists":readlists, "notificationsNum": notificationsNum, "chatsNum":chatsNum})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "minds/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "minds/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "minds/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            title = str(user.username)+'`s reading list'
            readlist = ReadList(reader=user, title=title)
            readlist.save()
            creadlist = CurrentRead(reader=user)
            creadlist.save()
        except IntegrityError:
            return render(request, "minds/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "minds/register.html")


# write 
@login_required
def write(request):
    if request.user.is_authenticated:
        notificationsNum = len(Notification.objects.filter(owner=request.user, look=0))
    if request.method == 'POST':
        user = request.user
        story = 0
        if 'img' in request.FILES:
            image = request.FILES['img']
            story = Story(writer=user, title=request.POST["title"], description=request.POST["desc"], category=request.POST["category"], cover=image)
            story.save()
        else:
            story = Story(writer=user, title=request.POST["title"], description=request.POST["desc"], category=request.POST["category"], cover=NULL)
            story.save()
        text = str(request.user.username) + " begins writting New Story"
        url = "../story/"+str(story.id)
        followers = Follow.objects.filter(owner=request.user)
        for follower in followers:
            n = Notification(owner=follower.userF, text=text, url=url)
            n.save()
        return redirect("../../write/"+str(story.id)+"/"+str(1))
    return render(request, "minds/write.html", {"notificationsNum": notificationsNum})


def writeChapter(request, sid, cid):
    if request.user.is_authenticated:
        notificationsNum = len(Notification.objects.filter(owner=request.user, look=0))
    if request.method == 'POST':
        story = Story.objects.get(id=sid)
        chapter = Chapter(story=story, title=request.POST["title"], content=request.POST["content"])
        chapter.save()
        text = str(request.user.username) + " published New Chapter"
        url = "../../../story/"+str(sid)
        sendNotifications(request, text, url, story)
        return redirect("../../../story/"+str(sid))
    return render(request, "minds/writeChapter.html", {"sid":sid, "cid":cid, "notificationsNum": notificationsNum})


def story(request, sid):
    story = Story.objects.get(id=sid)
    chapters = Chapter.objects.filter(story=story)
    if request.user.is_authenticated:
        notificationsNum = len(Notification.objects.filter(owner=request.user, look=0))
    return render(request, "minds/story.html", {"story":story, "chapters":chapters, "len":len(chapters)+1, "notificationsNum": notificationsNum})


def editChapter(request, cid):
    chapter = Chapter.objects.get(id=cid)
    if request.user.is_authenticated:
        notificationsNum = len(Notification.objects.filter(owner=request.user, look=0))
    if request.method == 'POST':
        chapter.title = request.POST["title"] 
        chapter.content = request.POST["content"]
        chapter.save()
        # chapter.save(update_fields=['title', 'content'])
        text = str(request.user.username) + " edited a Chapter in " + chapter.story.title
        url = "../../editChapter/"+str(chapter.id)
        sendNotifications(request, text, url, chapter.story)
        return redirect("../../story/"+str(chapter.story.id))
    if (request.user.id == chapter.story.writer.id):
        return render(request, "minds/editChapter.html", {"chapter":chapter, "notificationsNum": notificationsNum})
    else:
        return render(request, "minds/viewChapter.html", {"chapter":chapter, "notificationsNum": notificationsNum})

def sendNotifications(request, text, url, story):
    followers = Follow.objects.filter(owner=request.user)
    users = []
    for follower in followers:
        if(follower.userF not in users):
            users.append(follower.userF)
    readlists = Contain.objects.filter(story = story)
    for r in readlists:
        if(r.readlist.reader not in  users):
            users.append(r.readlist.reader)
    currentReads = CurrentContain.objects.filter(story = story)
    for c in currentReads:
        if(c.cuurentRead.reader not in users):
            users.append(c.cuurentRead.reader)
    archives = Archive.objects.filter(story = story)
    for a in archives:
        if(a.reader not in users):
            users.append(a.reader)
    for u in users:
        n = Notification(owner=u, text=text, url=url)
        n.save()

# read
@csrf_exempt
@login_required
def addToReadlist(request, sid):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    story = Story.objects.get(id=sid)
    # get body
    data = json.loads(request.body)
    for readlist in data.get("checkList"):
        if (readlist == "mine"):
            print("yes")
            cr = CurrentRead.objects.get(reader=request.user)
            try:
                CurrentContain.objects.get(cuurentRead=cr, story=story)
                print("y")
            except CurrentContain.DoesNotExist: 
                crc = CurrentContain(cuurentRead=cr, story=story)
                crc.save()
        else:
            r = ReadList.objects.get(reader=request.user, title=readlist)
            try:
                Contain.objects.get(readlist=r, story=story)
                print("y")
            except Contain.DoesNotExist: 
               rc = Contain(readlist=r, story=story)
               rc.save()
            
    return JsonResponse({"message": "1"}, status=400)

def checkList(request, sid):
    readlists = ReadList.objects.filter(reader = request.user)
    story = Story.objects.get(id = sid)
    checked = []
    for readlist in readlists:
        try:
            Contain.objects.get(readlist=readlist, story=story)
            checked.append(readlist)
        except Contain.DoesNotExist: 
            pass
    try:
        CurrentContain.objects.get(cuurentRead=CurrentRead.objects.get(reader=request.user), story=story)
        checked.append(ReadList(reader=request.user, title="mine"))
    except CurrentContain.DoesNotExist: 
        pass
    return JsonResponse([readlist.serialize() for readlist in checked], safe=False)


def showReadinglists(request):
    readlists = ReadList.objects.filter(reader = request.user).order_by("-created_at")
    if request.user.is_authenticated:
        notificationsNum = len(Notification.objects.filter(owner=request.user, look=0))
    lists_stories = []
    for readlist in readlists:
        length = len(Contain.objects.filter(readlist = readlist))
        lists_stories.append([readlist, length])
    return render(request, "minds/showReadinglists.html", {"readlists": lists_stories, "notificationsNum": notificationsNum})

def addReadList(request, name):
    readlist = ReadList(reader=request.user, title=name)
    readlist.save()
    return JsonResponse({"message": "1"}, status=400)


def showReadlist(request, rid):
    readlist = ReadList.objects.get(id = rid)
    stories = Contain.objects.filter(readlist = readlist)
    if request.user.is_authenticated:
        notificationsNum = len(Notification.objects.filter(owner=request.user, look=0))
    return render(request, "minds/showReadlist.html", {"stories": stories, "notificationsNum": notificationsNum})

def showCurrentReads(request):
    currentReads = CurrentContain.objects.filter(cuurentRead=CurrentRead.objects.get(reader=request.user)).order_by("-created_at")
    readlists = ReadList.objects.filter(reader = request.user)
    if request.user.is_authenticated:
        notificationsNum = len(Notification.objects.filter(owner=request.user, look=0))
    return render(request, "minds/showCurrentReads.html", {"currentReads": currentReads, "readlists": readlists, "notificationsNum": notificationsNum})

def archive(request, cid):
    currentread = CurrentContain.objects.get(id=cid)
    archive = Archive(reader=request.user, story=currentread.story)
    archive.save()
    currentread.delete()
    return redirect("../../showCurrentReads")

def showArchives(request):
    archiveList = Archive.objects.filter(reader=request.user).order_by("-created_at")
    readlists = ReadList.objects.filter(reader = request.user)
    if request.user.is_authenticated:
        notificationsNum = len(Notification.objects.filter(owner=request.user, look=0))
    return render(request, "minds/showArchives.html", {"archiveList": archiveList, "readlists": readlists, "notificationsNum":  notificationsNum})

def unarchive(request, aid):
    archived = Archive.objects.get(id = aid)
    currentread = CurrentContain(cuurentRead=CurrentRead.objects.get(reader=request.user), story=archived.story)
    currentread .save()
    archived.delete()
    return redirect("../../showArchives")


# chats
def chats(request):
    user = request.user
    chats = Chat.objects.filter(Q(user1=user) | Q(user2=user)).order_by("-created_at")
    chats_messages = []
    for chat in chats:
        messages = Message.objects.filter(Q(sender=chat.user1, reciever=chat.user2) | Q(sender=chat.user2, reciever=chat.user1)).order_by('created_at')
        if(chat.user1 != user):
            recievedMessages = len(Message.objects.filter(sender=chat.user1, reciever=user, read=0))
        else:
            recievedMessages = len(Message.objects.filter(sender=chat.user2, reciever=user, read=0))
        chats_messages.append([chat,messages[len(messages) - 1], recievedMessages])
    # print(chats_messages)
    recievedMessages = Message.objects.filter(reciever=request.user, look=0)
    for m in recievedMessages:
        m.look = 1
        m.save(update_fields=['look'])
    if request.user.is_authenticated:
        notificationsNum = len(Notification.objects.filter(owner=request.user, look=0))
    return render(request, 'minds/chats.html',{"chats_messages":chats_messages, "notificationsNum": notificationsNum})

def chat(request,uid):
    sender = request.user
    reciever = User.objects.get(id=uid)
    messages=[]
    if request.user.is_authenticated:
        notificationsNum = len(Notification.objects.filter(owner=request.user, look=0))
    try:
        chat = Chat.objects.get(Q(user1=sender, user2=reciever) | Q(user1=reciever, user2=sender))
        messages = Message.objects.filter(chat=chat)
        recievedMessages = Message.objects.filter(chat=chat, reciever=request.user)
        for r in recievedMessages:
            r.read = 1
            r.save(update_fields=['read'])
        return render(request, 'minds/chat.html',{"reciever":reciever, "messages":messages, "notificationsNum": notificationsNum})
    except Chat.DoesNotExist:
        print("chats")
        return render(request, 'minds/chat.html',{"reciever":reciever, "messages":messages, "notificationsNum": notificationsNum})

# search
def search(request,name):
	users = User.objects.filter(Q(username__contains=name) | Q(email__contains=name) | Q(first_name__contains=name) | Q(last_name__contains=name))
	return JsonResponse([user.serialize() for user in users], safe=False)

@csrf_exempt
def send_message(request):
	if request.method == "POST":
		data = json.loads(request.body)
		message = data.get("message")
		# file = data.get("file")
		id = data.get("id")
		sender = request.user
		reciever = User.objects.get(id=id)
		chat=""
		new_message = ""
		try:
			chat = Chat.objects.get(Q(user1=sender, user2=reciever) | Q(user1=reciever, user2=sender))
		except Chat.DoesNotExist:
			chat = Chat(user1=sender, user2=reciever)
			chat.save()
		if(message):
			new_message = Message(sender=sender, reciever=reciever, chat=chat, message=message)
			new_message.save()
		else:
			return JsonResponse({"error": "should send a message"}, status=400)
		return JsonResponse({"message": new_message.serialize()}, status=400)

from datetime import datetime

def send(request):
	if request.method == 'POST':
		message = request.POST["message"]
		file = ""
		original_name=""
		reciver_id = request.POST["id"]
		sender = request.user
		reciever = User.objects.get(id=reciver_id)
		if 'file' in request.FILES:
			file = request.FILES['file']
			original_name = file.name
			now = datetime.now()
			dt_string = now.strftime("%d%m%Y%H%M%S")
			print("date and time =", dt_string)
			file.name = dt_string+"."+(file.name).split(".")[1]
		print(message)
		print(reciver_id)
		chat=""
		try:
			chat = Chat.objects.get(Q(user1=sender, user2=reciever) | Q(user1=reciever, user2=sender))
		except Chat.DoesNotExist:
			chat = Chat(user1=sender, user2=reciever)
			chat.save()
		if(file and message):
			new_message = Message(sender=sender, reciever=reciever, chat=chat, message=message, file=file, original_name=original_name, name=file.name)
			new_message.save()
		elif(file and not message):
			new_message = Message(sender=sender, reciever=reciever, chat=chat, message=NULL, file=file, original_name=original_name, name=file.name)
			new_message.save()
		elif(not file and message):
			new_message = Message(sender=sender, reciever=reciever, chat=chat, message=message, file=NULL, original_name=original_name, name=NULL)
			new_message.save()
		else:
			return 'error'
		return redirect("../chat/"+str(reciver_id))

def upload(request, name, type):
	file=""
	if type == 1:
		file = open('media/files/'+str(name), 'rb')
	elif type == 2:
		file = open('media/lectures/'+str(name), 'rb')
	response = FileResponse(file)
	print(response)
	return response

# notifications
def showNotifications(request):
    notifications = Notification.objects.filter(owner=request.user).order_by("-created_at")
    for n in notifications:
        n.look = 1
        n.save(update_fields=['look'])
    return render(request, 'minds/showNotifications.html',{"notifications": notifications})

def markread(request, nid):
    n = Notification.objects.get(id=nid)
    n.read = 1
    n.save(update_fields=['read'])
    return JsonResponse({"message": "1"}, status=400)

# search
def searchForStory(request):
    storyName = request.GET["name"]
    stories = Story.objects.filter(Q(title__contains=storyName) | Q(category__contains=storyName)).order_by("-created_at")
    paginator = Paginator(stories, 10)
    page = request.GET.get('page')
    try:
        storiesList = paginator.page(page)
    except PageNotAnInteger:
        storiesList = paginator.page(1)
    except EmptyPage:
        storiesList = paginator.page(paginator.num_pages)
    readlists = ReadList.objects.filter(reader = request.user)
    if request.user.is_authenticated:
        notificationsNum = len(Notification.objects.filter(owner=request.user, look=0))
    return render(request, 'minds/searchForStory.html',{"storiesList": storiesList, "readlists":readlists, "notificationsNum": notificationsNum})


# profile
def profile(request, uid):
    puser = User.objects.get(id = uid)
    stories = Story.objects.filter(writer=puser).order_by('-created_at')
    # follow or unfollow
    follow = 0
    if request.user.is_authenticated: 
        if(request.user.id != puser.id):
            try:
                f = Follow.objects.get(userF=request.user, owner=puser)
                follow = 1
            except Follow.DoesNotExist:
                print("not exist")
        else:
            print("no")

    #  no. of followers
    numOfFollowers = 0
    try:
        f = Follow.objects.filter(owner=puser)
        numOfFollowers = f.count()
    except Follow.DoesNotExist:
        print("not exist")
    # no. of following
    numOfFollowings = 0
    try:
        f = Follow.objects.filter(userF=puser)
        numOfFollowings = f.count()
    except Follow.DoesNotExist:
        print("not exist")
    
    if request.user.is_authenticated:
        notificationsNum = len(Notification.objects.filter(owner=request.user, look=0))
    return render(request, "minds/profile.html", 
    {'puser':puser, 'stories':stories, "follow":follow, "numOfFollowers":numOfFollowers, "numOfFollowings": numOfFollowings, "notificationsNum": notificationsNum
    })

@login_required
def follow(request, uid):
    puser = User.objects.get(id = uid)
    f = Follow(userF=request.user, owner=puser)
    f.save()
    text = str(request.user.username) + " start following you"
    url = "../../profile/"+str(request.user.id)
    n = Notification(owner=puser, text=text, url=url)
    n.save()
    return redirect("../../profile/"+str(uid))

@login_required
def unfollow(request, uid):
    puser = User.objects.get(id = uid)
    f = Follow.objects.get(userF=request.user, owner=puser)
    f.delete()
    return redirect("../../profile/"+str(uid))
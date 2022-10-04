from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    # write
    path("write", views.write, name="write"),
    path("write/<int:sid>/<int:cid>", views.writeChapter, name="writeChapter"),
    path("story/<int:sid>", views.story, name="story"),
    path("editChapter/<int:cid>", views.editChapter, name="editChapter"),
    # read
    path("addToReadlist/<int:sid>", views.addToReadlist, name="addToReadlist"),
    path("checkList/<int:sid>", views.checkList, name="checkList"),
    path("showReadinglists", views.showReadinglists, name="showReadinglists"),
    path("addReadList/<str:name>", views.addReadList, name="addReadList"),
    path("showReadlist/<int:rid>", views.showReadlist, name="showReadlist"),
    path("showCurrentReads", views.showCurrentReads, name="showCurrentReads"),
    path("archive/<int:cid>", views.archive, name="archive"),
    path("showArchives", views.showArchives, name="showArchives"),
    path("unarchive/<int:aid>", views.unarchive, name="unarchive"),
    # chats
    path('chats', views.chats, name="chats"),
    path('chat/<int:uid>', views.chat, name="chat"),
    path('search/<str:name>', views.search, name="search"),
    path('send_message', views.send_message, name="send_message"),
    # notifications
    path('showNotifications', views.showNotifications, name="showNotifications"),
    path('markread/<int:nid>', views.markread, name="markread"),
    # search
    path('searchForStory', views.searchForStory, name="searchForStory"),
    # profile
    path("profile/<int:uid>", views.profile, name="profile"),
    path("follow/<int:uid>", views.follow, name="follow"),
    path("unfollow/<int:uid>", views.unfollow, name="unfollow"),
]
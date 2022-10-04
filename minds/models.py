from django.db import models
from unicodedata import category
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
	def serialize(self):
		return {
			"id": self.id,
			"email":self.email,
			"username": self.username
	}

class Story(models.Model):
	writer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="writer")
	title = models.CharField(max_length=100)
	description = models.CharField(max_length=1000)
	category = models.CharField(max_length=64)
	cover = models.ImageField(upload_to='covers/')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


class Chapter(models.Model):
	story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name="story")
	title = models.CharField(max_length=100)
	content = models.CharField(max_length=10000)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class ReadList(models.Model):
    reader = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reader")
    title = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def serialize(self):
        return {
            "title": self.title
        }

class Contain(models.Model):
	readlist = models.ForeignKey(ReadList, on_delete=models.CASCADE, related_name="readerlist")
	story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name="readstory")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class CurrentRead(models.Model):
	reader = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creader")

class CurrentContain(models.Model):
	cuurentRead = models.ForeignKey(CurrentRead, on_delete=models.CASCADE, related_name="CurrentRead")
	story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name="creadstory")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)	


class Archive(models.Model):
	reader = models.ForeignKey(User, on_delete=models.CASCADE, related_name="areader")
	story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name="areadstory")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

# chats
class Chat(models.Model):
	user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user1", null=True)
	user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user2", null=True)
	created_at = models.DateTimeField(auto_now_add=True, null=True)

class Message(models.Model):
	sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
	reciever = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reciever")
	chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="chat")
	message = models.CharField(max_length=800,null=True)
	file = models.FileField(upload_to='files/',null=True)
	original_name = models.CharField(max_length=64 ,null=True)
	name = models.CharField(max_length=64 ,null=True)
	look = models.IntegerField(default = 0)
	read = models.IntegerField(default = 0)
	created_at = models.DateTimeField(auto_now_add=True, null=True)
	updated_at = models.DateTimeField(auto_now=True, null=True)
	def serialize(self):
		return {
			"id": self.id,
			"message":self.message
	}

# profile
class Follow(models.Model):
    userF = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userF", null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="fowner", null=True)

# notifications
class Notification(models.Model):
	owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="nowner", null=True)
	text =  models.CharField(max_length=100,null=True)
	url =  models.CharField(max_length=80,null=True)
	look = models.IntegerField(default = 0)
	read = models.IntegerField(default = 0)
	created_at = models.DateTimeField(auto_now_add=True, null=True)
	updated_at = models.DateTimeField(auto_now=True, null=True)
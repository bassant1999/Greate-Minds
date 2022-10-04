from xml.etree.ElementTree import Comment
from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Story)
admin.site.register(Chapter)
admin.site.register(ReadList)
admin.site.register(Contain)
admin.site.register(CurrentRead)
admin.site.register(CurrentContain)
admin.site.register(Archive)
admin.site.register(Notification)
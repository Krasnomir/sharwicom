from django.contrib import admin
from .models import Conversation, Message, Content, Rating

# Register your models here.

admin.site.register(Conversation)
admin.site.register(Message)
admin.site.register(Content)
admin.site.register(Rating)

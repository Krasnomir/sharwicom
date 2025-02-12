from django.contrib import admin
from .models import Conversation, Message, Content, Review, Post, Community

# Register your models here.

admin.site.register(Conversation)
admin.site.register(Message)
admin.site.register(Content)
admin.site.register(Review)
admin.site.register(Post)
admin.site.register(Community)

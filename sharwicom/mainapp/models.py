from django.db import models
from django.contrib.auth.models import User

class Conversation(models.Model):
    person1 = models.ForeignKey(User, related_name="conversations_as_person1", on_delete=models.CASCADE)
    person2 = models.ForeignKey(User, related_name="conversations_as_person2", on_delete=models.CASCADE)

class Message(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)

class Content(models.Model):
    url_name = models.CharField(max_length=50) # title in lowercase without spaces
    title = models.CharField(max_length=50)
    ratings = models.JSONField(default=dict)

class Rating(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.SmallIntegerField() # integers ranging from 1 to 5
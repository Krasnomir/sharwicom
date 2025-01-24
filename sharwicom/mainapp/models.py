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

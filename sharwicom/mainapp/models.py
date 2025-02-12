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

content_types = [
    'book',
    'movie',
    'song',
    'album',
    'video',
    'other'
]

class Content(models.Model):
    author = models.CharField(max_length=50, default="Author placeholder")
    url_name = models.CharField(max_length=50) # title in lowercase without spaces
    title = models.CharField(max_length=50)
    description = models.TextField(default="Description placeholder")
    type = models.CharField(max_length=20, default="book")
    ratings = models.JSONField(default=dict)

    def set_user_rating(self, user, rating):
        self.ratings[user.username] = rating
        self.save()

    def get_user_rating(self, user):
        return self.ratings.get(user.username, None)
    
class Review(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)

    summary = models.CharField(max_length=50)
    description = models.TextField()

    rating = models.SmallIntegerField(default=0)
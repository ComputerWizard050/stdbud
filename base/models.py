from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)
    avatar = models.ImageField(null=True, default="avatar.svg")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # hosts = models.ManyToManyField(User, related_name='hosts', null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    avatar = models.ImageField(null=True, default="avatar.svg")  # new
    participants = models.ManyToManyField(
        User, related_name='participants', blank=True)
    notallowed = models.ManyToManyField(
        User, related_name='notallowed', blank=True)
    cohosts = models.ManyToManyField(User, related_name='cohosts', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name

# message class before adding image or video
# class Message(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     room = models.ForeignKey(Room, on_delete=models.CASCADE)
#     body = models.TextField()
#     updated = models.DateTimeField(auto_now=True)
#     created = models.DateTimeField(auto_now_add=True)
#     likes = models.ManyToManyField(User, related_name='message_name')

#     class Meta:
#         ordering = ['-updated', '-created']

#     def __str__(self):
#         return self.body[0:50]


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField(null=True)
    uploadfile = models.ImageField(
        null=True, blank=True, upload_to='images/')  # upload_to
    isimg = models.BooleanField(null=True)  # default
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    # likes = models.ManyToManyField(
    # User, null=True, related_name='message_name')

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[0:50]


class Chatmessage(models.Model):
    fromuser = models.ForeignKey(
        User, related_name='fromuser', on_delete=models.CASCADE)
    touser = models.ForeignKey(
        User, related_name='touser', on_delete=models.CASCADE)
    body = models.TextField(null=True)
    uploadfile = models.ImageField(
        null=True, blank=True, upload_to='images/')  # upload_to
    isimg = models.BooleanField(null=True)  # default
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    # new
    def __str__(self):
        return self.body[0:50]


class Hascontactwith(models.Model):
    user = models.ForeignKey(
        User, related_name='user', on_delete=models.CASCADE)
    contactpersons = models.ManyToManyField(
        User, related_name='contactpersons', blank=True)

    # def __str__(self):
    #     return self.user

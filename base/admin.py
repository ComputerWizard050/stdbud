from django.contrib import admin


from .models import Room, Topic, Message, User,Chatmessage, Hascontactwith

admin.site.register(User)
admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)
admin.site.register(Chatmessage)
admin.site.register(Hascontactwith)

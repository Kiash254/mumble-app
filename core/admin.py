from django.contrib import admin
from .models import Room,Message,Topic
# Register your models here.


admin.site.site_header = 'Admin panel room'
admin.site.site_title = 'Admin panel room'
admin.site.index_title = 'Admin panel room'
admin.site.register(Room)
admin.site.register(Message)
admin.site.register(Topic)
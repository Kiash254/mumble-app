from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Room(models.Model):
    # host=models.ForeignKey('User',on_delete=models.CASCADE)
    # topic=models.CharField(max_length=100,null=True,blank=True)
    name = models.CharField(max_length=255,null=True,blank=True)
    description = models.TextField(max_length=1000,null=True,blank=True)
    # participants = models.ManyToManyField('User',related_name='rooms')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

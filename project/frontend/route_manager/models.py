from django.db import models
#import datetime
#import django.utils.timezone 

class Post(models.Model):
    ip = models.GenericIPAddressField()
    #mask = models.GenericIPAddressField(default="255.255.255.255")
    next_hop = models.GenericIPAddressField()
    community = models.CharField(max_length=100)
    #enabled = models.BooleanField(default=1)
    #created = models.DateTimeField(default=django.utils.timezone.now, blank=True)
    #modified = models.DateTimeField(default=django.utils.timezone.now, blank=True)

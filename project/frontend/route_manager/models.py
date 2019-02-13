from django.db import models

class Post(models.Model):
    ip = models.GenericIPAddressField()
    next_hop = models.GenericIPAddressField()
    community = models.CharField(max_length=100)

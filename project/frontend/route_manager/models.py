"""
Define the model used to create a new route.
"""
from django.db import models

class Post(models.Model):
    """
    New route model.
    """
    ip = models.GenericIPAddressField(protocol='IPv4')
    next_hop = models.GenericIPAddressField(protocol='IPv4')
    community = models.CharField(max_length=100)

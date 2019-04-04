"""
Define the model used to create a new route.
"""
from django.db import models
from django.core.validators import RegexValidator

validator_ip = '^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(/(3[0-2]|[1-2][0-9]|[0-9]))$'
validator_com = '^(([0-9]|[0-9][0-9])\:([0-9][0-9]|[0-9]))$'


class Post(models.Model):
    """
    New route model.
    """
    ip = models.CharField(max_length=18, validators=[RegexValidator(
        validator_ip, message="Exemple: 192.168.0.1/32")])
    next_hop = models.GenericIPAddressField(protocol='IPv4')
    community = models.CharField(max_length=5, validators=[RegexValidator(
        validator_com, message="Exemple: 45:50")], blank=True, null=True)

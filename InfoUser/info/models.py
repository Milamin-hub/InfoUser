from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    name = models.CharField(max_length=15)
    username = models.CharField(max_length=20)
    state_id = models.IntegerField()

    def __str__(self):
        return self.name


from django.contrib.auth.models import User
from django.db import models


class SecretHashCode(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE, related_name='hashcode')
    hashcode = models.CharField(max_length=12)

    def __str__(self):
        return self.hashcode
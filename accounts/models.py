from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    role = models.CharField(max_length=50, default="عميل قهوة") # الصلاحيات

    def __str__(self):
        return f"{self.user.username} - {self.role}"
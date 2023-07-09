from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete = models.CASCADE)
    avatar = models.ImageField(upload_to = "profile_images",default= "default.jpg")
    address = models.CharField(max_length = 250,blank= False, null = False)
    phone = models.CharField(max_length = 10, blank=False, null= False)


    def __str__(self):
        return self.user.username
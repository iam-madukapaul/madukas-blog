from django.db import models
from django.contrib.auth.models import User



# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  
    name = models.CharField(max_length=200)
    profile_picture = models.ImageField(upload_to='img', default='default.jpg')
    username = models.CharField(max_length=200)
    profession = models.CharField(max_length=200)
    email = models.EmailField()
    about_me = models.TextField(max_length=200)  
 
    def __str__(self):
        return self.username
    
    # def save(self):
    #     super().save()

    #     img = Image.open(self.profile_picture.path)

    #     if img.height > 200 or img.width > 200:
    #         output_size = (200, 200)
    #         img.thumbnail(output_size)
    #         img.save(self.profile_picture.path)
    
    
    

    


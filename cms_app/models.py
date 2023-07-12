from django.db import models
from tinymce.models import HTMLField 
import uuid
from profiles.models import UserProfile
from PIL import Image
from django.contrib.auth.models import User 
import readtime

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='img')
    body = HTMLField()
    sno = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    slug = models.SlugField()
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, blank=True, null=True)

    def get_readtime(self):
        result = readtime.of_text(self.body)
        return result.text


    def __str__(self):
        return self.title
    
    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     img = Image.open(self.image.path)
    #     if img.height > 300 or img.width > 300:
    #         output_size = (300,300)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)
    
class Category(models.Model):
    title = models.CharField(max_length=200)
    sno = models.AutoField(primary_key=True)
    slug = models.SlugField()

    def __str__(self):
        return self.title 
    

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_comments', blank=True)
    dislikes = models.ManyToManyField(User, related_name='disliked_comments', blank=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"Comment by {self.author} on {self.post}"

class Reply(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_replies', blank=True)
    dislikes = models.ManyToManyField(User, related_name='disliked_replies', blank=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"Reply by {self.author} on {self.comment.post}"
    
    
    
    
    





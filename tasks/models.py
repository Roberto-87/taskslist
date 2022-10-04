from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    title= models.CharField(max_length=200)
    description=models.TextField(max_length=1000)
    created= models.DateTimeField(auto_now_add=True)
    date_completed= models.DateTimeField(null= True, blank=True)
    Low_importance= models.BooleanField(default=False)   
    medium_importance= models.BooleanField(default=False)   
    high_importance=models.BooleanField(default=False) 
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    
    
    def __str__(self):
      return self.title  + '- followed by ' + self.user.username
from django.db import models
from django.contrib.auth.models import User

class TaskList(models.Model):
    
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(User, on_delete= models.CASCADE, default=None)
    task = models.CharField(max_length=100)
    done = models.BooleanField(default = False)
    
    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.task
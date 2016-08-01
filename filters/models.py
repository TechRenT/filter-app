from django.db import models

# Create your models here.
class Filter(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    keyword = models.CharField(max_length=255)
    
    def __str__(self):
        return self.keyword

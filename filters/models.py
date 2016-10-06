from django.core.urlresolvers import reverse
from django.db import models


# Create your models here.
class Filter(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    order = models.IntegerField(default=0)
    keyword = models.CharField(max_length=255)
    
    def __str__(self):
        return self.keyword

    def get_absolute_url(self):
        return reverse("filter:keywords_cbv")

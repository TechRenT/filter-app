from django.contrib.auth.models import User
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


class VRPage(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Keyword(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)
    vrpage = models.ForeignKey(VRPage)

    def __str__(self):
        return self.name


class LinkedinProfile(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    profile_link = models.URLField(max_length=200)
    checker = models.ForeignKey(User)

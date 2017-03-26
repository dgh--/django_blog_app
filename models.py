from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from django.utils import timezone


class Post(models.Model):
    title = models.CharField(max_length = 100, null = False, unique=True)  
    body = models.TextField()
    posted = models.DateTimeField(db_index = True, default = timezone.now)

    def formatted_time(self):
        return self.posted.strftime('%d %b %Y at %X')

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey('Post', related_name = 'comments', on_delete = models.CASCADE)
    author = models.CharField(max_length = 200)
    text = models.TextField()
    created = models.DateTimeField(db_index = True, default = timezone.now)

    def formatted_time(self):
        return self.created.strftime('%d %b %Y at %X')

    def __str__(self):
        return self.text
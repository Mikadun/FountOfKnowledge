from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from tinymce.models import HTMLField


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = HTMLField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    journal = models.CharField(blank=True, max_length=150)
    volume = models.IntegerField(null=True)
    number = models.IntegerField(null=True)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ["-date"]


class Comment(models.Model):
    content = HTMLField()
    date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.content

    class Meta:
        ordering = ["-date"]

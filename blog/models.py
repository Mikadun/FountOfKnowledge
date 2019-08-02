from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from tinymce.models import HTMLField

import datetime
YEAR_CHOICES = [(r,r) for r in range(1950, datetime.date.today().year+1)]

class Post(models.Model):
	title = models.CharField(max_length=100)
	content = HTMLField()
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	journal = models.CharField(max_length=150)
	volume = models.IntegerField()
	number = models.IntegerField()
	date = models.IntegerField(choices=YEAR_CHOICES)
	file = models.FileField(upload_to = 'files/', null=True, max_length=1e3)

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

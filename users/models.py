from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    image = models.ImageField(default='default.png', upload_to='profile_pics')
    biography = models.TextField(blank=True)
    organization = models.CharField(max_length=150, blank=True)
    position = models.CharField(max_length=100, blank=True)
    degree = models.CharField(max_length=100, blank=True)
    link = models.URLField(blank=True)
    ORCID = models.CharField(max_length=100, blank=True)

    access = models.CharField(
        choices = [('Пользователь', 'Пользователь'),
            ('Модератор', 'Модератор'),
            ('Администратор', 'Администратор')
        ],
        default = 'standart',
        max_length = 20
    )

    def __str__(self):
        return f'{self.user.username} profile'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 150 or img.width > 150:
            output_size = (150, 150)
            img.thumbnail(output_size)
            img.save(self.image.path)

class Grant(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    year_from = models.IntegerField()
    year_to = models.IntegerField()
    fund = models.CharField(max_length=200)
    amount = models.IntegerField()
    link = models.URLField(blank=True)

    class Meta:
        ordering = ['amount']
        app_label = 'users'

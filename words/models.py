from django.db import models

# Create your models here.
from django.conf import settings


class Word(models.Model):
    eng = models.CharField(max_length=200)
    tr = models.TextField(null=True)
    rus = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='word_owner', null=True)
    favorites = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Fav', related_name='favorite_words')

    def __str__(self):
        return self.eng


class Fav(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('word', 'user')

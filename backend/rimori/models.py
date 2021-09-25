from django.db import models

# Create your models here.
class Word(models.Model):
    word = models.CharField(max_length=36)
    tail = models.CharField(max_length=12)
    index = models.IntegerField(default=0)
    vowel = models.CharField(max_length=1)
    def __str__(self):
        return self.word
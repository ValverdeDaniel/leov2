from django.db import models
from datetime import datetime

# Create your models here.
class Options(models.Model):
    ticker = models.CharField(max_length=200)
    price = models.IntegerField()
    date = models.DateTimeField(default=datetime.now, blank=True)
    def __str__(self):
        return self.ticker
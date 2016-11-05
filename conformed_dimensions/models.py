from django.db import models


class ZipCode(models.Model):
    zip_code = models.CharField(max_length=5)
    state_abrev = models.CharField(max_length=2)
    lat = models.FloatField()
    lon = models.FloatField()
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=50)
    distance = models.FloatField(default=0)
    
    def __str__(self):
        return "%s" % self.zip_code

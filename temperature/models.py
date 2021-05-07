from django.db import models

class tempImage(models.Model):
    temp = models.FloatField(blank=True , primary_key = True)
    tempimg= models.ImageField(upload_to='tempimages/', verbose_name="")
    # # pathway to the image

    def __str__(self):
        return str(self.tempimg)


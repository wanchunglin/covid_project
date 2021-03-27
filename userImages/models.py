from django.db import models
from users.models import User

class Image(models.Model):
    info = models.OneToOneField(User, on_delete=models.CASCADE,blank = True)
    
    imagefile= models.ImageField(upload_to='images/', verbose_name="")
    
    # # pathway to the image

    def __str__(self):
        return str(self.imagefile)

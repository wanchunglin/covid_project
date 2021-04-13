from django.db import models
from users.models import User

class Image(models.Model):
    info = models.OneToOneField(User, on_delete=models.CASCADE, blank = True, primary_key = True)
    imagefile= models.ImageField(upload_to='images/', verbose_name="")
    faceEmbedding = models.BinaryField()
    
    # # pathway to the image

    def __str__(self):
        return str(self.imagefile)

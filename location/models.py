from django.db import models
from users.models import User
from datetime import datetime

class EE(models.Model):
	userID = models.ForeignKey(User, on_delete=models.CASCADE)
	arriveTime = models.DateTimeField(default=datetime.now)

class ED(models.Model):
	userID = models.ForeignKey(User, on_delete=models.CASCADE)
	arriveTime = models.DateTimeField(default=datetime.now)	

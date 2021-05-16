from django.db import models
from users.models import User
from django.utils import timezone

class EE(models.Model):
	userID = models.ForeignKey(User, on_delete=models.CASCADE)
	arriveTime = models.DateTimeField(default=timezone.now)
	temp = models.FloatField()
class ED(models.Model):
	userID = models.ForeignKey(User, on_delete=models.CASCADE)
	arriveTime = models.DateTimeField(default=timezone.now)
	temp = models.FloatField()
class BOAI(models.Model):
	userID = models.ForeignKey(User, on_delete=models.CASCADE)
	arriveTime = models.DateTimeField(default=timezone.now)
	temp = models.FloatField()

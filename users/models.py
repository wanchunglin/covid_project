from django.db import models

class User(models.Model):
	userID = models.CharField(max_length=10, primary_key=True)
	userName = models.CharField(max_length=20)
	phone = models.CharField(max_length=10)
	email = models.CharField(max_length=100)
	password = models.CharField(max_length = 100)
	verified = models.BooleanField(default=False)
	# birthday = models.DateField(blank=True, null=True)
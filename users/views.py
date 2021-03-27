from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User
import json

def index(request):
    return HttpResponse("Hello, world. You're at the users index.")

def login(request):
	return JsonResponse({'status': 'temp'})

def logout(request):
	return JsonResponse({'status': 'temp'})

@csrf_exempt
def register(request):
	# name, userID, phone, email, password, picture
	if request.method == 'POST':
		print(request.body.decode('utf-8'))
		payload = json.loads(request.body.decode('utf-8'))
		print("the payload is: ", payload)
		
		newUser = User(userID=payload['userID'], 
		userName=payload['userName'],
		phone=payload['phone'],
		email=payload['email'],
		password = payload['password'])
		
		newUser.save()
		return JsonResponse({"status":"ok"})

	else:
		print("not a post request")
		# return JsonResponse({'status': 'This is not a post request'})
		return JsonResponse({"status":"failed"})

def verify(request):
	return JsonResponse({'status': 'temp'})
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import ED, EE
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from users.models import User
import json

def index(request):
    return HttpResponse("Hello, world. You're at the location index.")

@csrf_exempt
def locationAdd(request):
    print("get request: ", request)
    if request.method == 'POST':
        payload = json.loads(request.body)
        print("the payload is: ", payload)

        foundUser = User.objects.get(userID=payload['userID'])
        if foundUser is not None:
            if payload['location'] == "EE":
                newArrive = EE(userID=foundUser)
                newArrive.save()
            elif payload['location'] == "ED":
                newArrive = ED(userID=foundUser)
                newArrive.save()
        return JsonResponse({"status":"ok"})
        # return HttpResponse("I got your post request")

    else:
        print("not a post request")
        # return JsonResponse({'status': 'This is not a post request'})
        return HttpResponse("This is not a post request")
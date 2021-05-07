from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse, HttpRequest
from .models import tempImage
from django.views.decorators.csrf import csrf_exempt
from .forms import tempForm
import json
# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


@csrf_exempt
def addTemp(request):
    if request.method == 'POST':
        form = tempForm(request.POST, request.FILES)
        print(request.FILES)
        print(request.POST['temp'])

        if form.is_valid():
            newtemp = tempImage(tempimg=request.FILES['tempimg'],temp = request.POST['temp'])
            newtemp.save()
            return JsonResponse({"status":"ok"})
        else:
            print(form.errors)
            return JsonResponse({"status":"addImage fail"})
    else:
        return JsonResponse({"status":"not a post request"})
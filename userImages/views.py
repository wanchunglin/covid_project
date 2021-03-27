from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse, HttpRequest
from .models import Image
from django.views.decorators.csrf import csrf_exempt
from .forms import ImageForm
from users.models import User

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def showImage(request):

    lastimage= Image.objects.last()

    imagefile= lastimage.imagefile


    form= ImageForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()

    
    context= {'imagefile': imagefile,
              'form': form
              }
    return render(request, 'Blog/images.html', context)

@csrf_exempt
def addImage(request):
    if request.method == 'POST':
        form = ImageForm(request.POST,request.FILES)
        print("===================================")
        
        print(request.FILES['imagefile'].name)
        print(form.is_valid())
        print(form.errors)
        if form.is_valid():
            imageuser = User.objects.get(userID = request.FILES['imagefile'].name[:-4])
            # print(imageuser)
            newimage = Image(info = imageuser, imagefile = request.FILES['imagefile'])
            newimage.save()
            return JsonResponse({"status":"ok"})
        
    
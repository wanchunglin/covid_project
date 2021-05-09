from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse, HttpRequest
from .models import Image as userImage
from django.views.decorators.csrf import csrf_exempt
from .forms import ImageForm
from users.models import User
import json

# face verification with the VGGFace2 model
from matplotlib import pyplot
from PIL import Image
from numpy import asarray
from scipy.spatial.distance import cosine
from mtcnn.mtcnn import MTCNN
from keras_vggface.vggface import VGGFace
from keras_vggface.utils import preprocess_input
import pickle

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

        form = ImageForm(request.POST, request.FILES)
        # print(f'request payload is {request.payload}')
        print(f'request file is {request.FILES}')
        print("===================================")
        
        print(request.FILES['imagefile'].name)
        # print(form.is_valid())
        # print(form.errors)
        form = ImageForm(request.POST,request.FILES)

        print(f'request file is {request.FILES}')
        print("===================================")
        print(request.POST)
        print(request.FILES['imagefile'].name)
        print(form.is_valid())
        print(form.errors)

        if form.is_valid():
            imageuser = User.objects.get(userID=request.FILES['imagefile'].name[:-4])
            # print(imageuser)
            newimage = userImage(info=imageuser, imagefile=request.FILES['imagefile'])
            
            newimage.faceEmbedding = getFaceEmbedding(request.FILES['imagefile'])

            newimage.save()
            return JsonResponse({"status":"ok"})
        else:
            return JsonResponse({"status":"addImage fail"})
    else:
        return JsonResponse({"status":"not a post request"})

def checkFaceEmbedding(request):
    if request.method == 'GET':
        payload = json.loads(request.body.decode('utf-8'))
        getImage = userImage.objects.get(info=payload['userID'])
        embeddingArray = pickle.loads(getImage.faceEmbedding)
        print(f'the embedding array has shape {embeddingArray.shape}')
        return JsonResponse({"status":"ok"})
    else:
        return JsonResponse({"status":"not a post request"})

def getFaceEmbedding(file):
    # extract faces
    face = [extract_face(file)]
    # convert into an array of samples
    sample = asarray(face, 'float32')
    # prepare the face for the model, e.g. center pixels
    sample = preprocess_input(sample, version=2)
    # create a vggface model
    model = VGGFace(model='resnet50', include_top=False, input_shape=(224, 224, 3), pooling='avg')
    # perform prediction
    yhat = model.predict(sample)
    # convert nparray to pickle string
    dump = yhat.dumps()
    return dump

def extract_face(filename, required_size=(224, 224)):
    # load image from file
    pixels = pyplot.imread(filename)
    # create the detector, using default weights
    detector = MTCNN()
    # detect faces in the image
    results = detector.detect_faces(pixels)
    # extract the bounding box from the first face
    x1, y1, width, height = results[0]['box']
    x2, y2 = x1 + width, y1 + height
    # extract the face
    face = pixels[y1:y2, x1:x2]
    # resize pixels to the model size
    image = Image.fromarray(face)
    image = image.resize(required_size)
    face_array = asarray(image)
    return face_array
        
    
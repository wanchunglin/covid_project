from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .models import User
import smtplib, ssl, json, time
from datetime import datetime
from random import seed,randint
from userImages.models import Image as userImage

# face verification with the VGGFace2 model
from matplotlib import pyplot
from PIL import Image
from numpy import asarray
from scipy.spatial.distance import cosine
from mtcnn.mtcnn import MTCNN
from keras_vggface.vggface import VGGFace
from keras_vggface.utils import preprocess_input
import pickle

verification = {}

def index(request):
    return HttpResponse("Hello, world. You're at the users index.")

@csrf_exempt
def login(request):
    if request.method == 'POST':
        payload = json.loads(request.body.decode('utf-8'))
        print("the payload is: ", payload)
        try:
            getUser = User.objects.get(userID=payload['userID'], password=payload['password'])
            if not getUser.verified:
                return JsonResponse({'status': 'not verified'})
            return JsonResponse({'status': 'ok'})
        except ObjectDoesNotExist:
            print("login failed")
            return JsonResponse({'status': 'fail'})


@csrf_exempt
def register(request):
    # name, userID, phone, email, password, picture
    if request.method == 'POST':
        seed(datetime.now())
        payload = json.loads(request.body.decode('utf-8'))
        print("the payload is: ", payload)

        newUser = User(userID=payload['userID'], 
                        userName=payload['userName'],
                        phone=payload['phone'],
                        email=payload['email'],
                        password=payload['password'])

        try:
            newUser.save(force_insert=True)
        except Exception as e:
                error = "error: {}".format(e)
                print(error)
                if("Duplicate" in error):
                    return JsonResponse({"status":"repeat user"})

        key = ""
        for x in range(6):
            key += str(randint(0,9))
        send_mail(payload['email'],key)
        verification[payload['userID']] = key
        print(verification)
        
        return JsonResponse({"status":"ok"})

    else:
        print("not a post request")
        # return JsonResponse({'status': 'This is not a post request'})
        return JsonResponse({"status":"request failed"})

@csrf_exempt
def verify(request):
    if request.method == 'POST':
        payload = json.loads(request.body.decode('utf-8'))
        print("the payload is: ", payload)

        if verification[payload['userID']] == payload['verify']:
            del verification[payload['userID']]
            verifiedUser = User.objects.get(userID=payload['userID'])
            print(f'find user {verifiedUser}')
            verifiedUser.verified = True
            verifiedUser.save()
            return JsonResponse({'status': 'ok'})
        else:
            return JsonResponse({'status': 'fail'})

@csrf_exempt
def faceMatching(request):
	if request.method == 'POST':
		'''
		try:
			ID = request.POST.get('ID')
			print("ID is ", ID)
			fileName = request.POST.get('faceImage')
			print("fileName is ", fileName)
			temperature = request.POST.get('temperature')
			print("temperature is ", temperature)
			imageFile = request.FILES.get('imagefile')
			print("imageFile is ", imageFile)
		except:
			print("exception happens")
		'''
		ID = request.POST.get('ID')
		print("ID is ", ID)
		temperature = request.POST.get('temperature')
		print("temperature is ", temperature)
		imageFile = request.FILES.get('imagefile')
		print("imageFile is ", imageFile)
		fileName = default_storage.save('face_recognition/'+imageFile.name, ContentFile(imageFile.read()))
		print("fileName is ", fileName)
		
		# face recognition
		# get faceEmbedding from table
		time.sleep(0.5)
		target_embedding = userImage.objects.get(user=ID).faceEmbedding
		faceIsMatch = performFaceRecognition(target=target_embedding, inputImg=fileName)
		if faceIsMatch:
			queryUser = User.objects.get(userID=ID)
			response = {
						"userID": queryUser.userID,
						"userName": queryUser.userName,
						"phone": queryUser.phone,
						"email": queryUser.email,
						"temperature": temperature
						}
			return JsonResponse(response)
		else:
			return JsonResponse({"status": "Face is not matched"})

def performFaceRecognition(target, inputImg):
    # filenames should be the photos we take at real time
    filenames = ['media/'+inputImg]
    # get embeddings file filenames
    embeddings = get_embeddings(filenames)
    # define the target embedding
    # get the faceEmbedding column from our database
    # and get the numpy array be pickle.loads()
    target_id = pickle.loads(target)

    # verify by comparing with the target
    print('start testing')
    return is_match(target_id, embeddings[0])

# extract a single face from a given photograph
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

# extract faces and calculate face embeddings for a list of photo files
def get_embeddings(filenames):
    # extract faces
    faces = [extract_face(f) for f in filenames]
    # convert into an array of samples
    samples = asarray(faces, 'float32')
    # prepare the face for the model, e.g. center pixels
    samples = preprocess_input(samples, version=2)
    # create a vggface model
    model = VGGFace(model='resnet50', include_top=False, input_shape=(224, 224, 3), pooling='avg')
    # perform prediction
    yhat = model.predict(samples)
    print(f'embedding shape = {yhat.shape}')
    return yhat

# determine if a candidate face is a match for a known face
def is_match(known_embedding, candidate_embedding, thresh=0.5):
    # calculate distance between embeddings
    score = cosine(known_embedding, candidate_embedding)
    print("Score is ", score)
    if score <= thresh:
        print('>face is a Match (%.3f <= %.3f)' % (score, thresh))
        return True
    else:
        print('>face is NOT a Match (%.3f > %.3f)' % (score, thresh))
        return False

def send_mail(receiver="", key=""):
    print("sending email")
    port = 465  # For SSL
    # password = input("Type your password and press enter: ")
    password = "yyh@RPITesing11042020"
    sender_email = "yyhrpitesting@gmail.com"
    message = """\
    Subject: Hi there from NYCU App\n

    Your verification code is {key}""".format(key=key)

    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server: # use port 465 at default
        server.login("yyhrpitesting@gmail.com", password)
        server.sendmail(sender_email, receiver, message)
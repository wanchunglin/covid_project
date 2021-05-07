from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from .models import User
import smtplib, ssl, json
from datetime import datetime
from random import seed,randint

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

def faceMatching(request):
    if request.method == 'GET':
        currentUser = request.GET.get('ID')
        print("the ID is: ", currentUser)
        currentTemperature = request.GET.get('temperature')
        print("the temperature is: ", currentTemperature)
        '''
        currentFaceImage = request.Get.get('faceImage')
        print("the faceImage is: ", currentFaceImage)
        '''

        # add face recognition here
        
        faceIsMatch = True
        if faceIsMatch:
            queryUser = User.objects.get(userID=currentUser)
            print(f'find user {queryUser}')
            response = {
                        "userID": queryUser.userID,
                        "userName": queryUser.userName,
                        "phone": queryUser.phone,
                        "email": queryUser.email
                        }
            return JsonResponse(response)
        else:
            return JsonResponse({"status": "Face is not matched"})

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
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User
import smtplib, ssl,json
from datetime import datetime
from random import seed,randint

verification = {}

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
        seed(datetime.now())
        payload = json.loads(request.body.decode('utf-8'))
        print("the payload is: ", payload)

        newUser = User(userID=payload['userID'], 
        userName=payload['userName'],
        phone=payload['phone'],
        email=payload['email'],
        password = payload['password'])

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
        return JsonResponse({"status":"failed"})

@csrf_exempt
def verify(request):
    if request.method == 'POST':
        payload = json.loads(request.body.decode('utf-8'))
        print("the payload is: ", payload)

        if verification[payload['userID']] == payload['verify']:
            return JsonResponse({'status': 'ok'})

def send_mail(receiver="", key=""):
    print("sending email")
    port = 465  # For SSL
    # password = input("Type your password and press enter: ")
    password = "yyh@RPITesing11042020"
    sender_email = "yyhrpitesting@gmail.com"
    message = """\
    Subject: Hi there from NYCU epdemic project App\n

    Your verification code is {key}""".format(key=key)

    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server: # use port 465 at default
        server.login("yyhrpitesting@gmail.com", password)
        server.sendmail(sender_email, receiver, message)
import firebase_admin
from django.conf import settings
from apps.accounts.models import CustomUser
from django.utils import timezone
from firebase_admin import auth, messaging, credentials
from rest_framework import authentication
from exceptions.firebase import *
from decouple import config


cred = credentials.Certificate({
        "type": "service_account",
        "project_id": config('FIREBASE_PROJECT_ID'),
        "private_key_id": config('FIREBASE_PRIVATE_KEY_ID'),
        "private_key": config('FIREBASE_PRIVATE_KEY').replace("\\n", "\n"),
        "client_email": config('FIREBASE_CLIENT_EMAIL'),
        "client_id": config('FIREBASE_CLIENT_ID'),
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": config('FIREBASE_CLIENT_CERT_URL')
    })

default_app = firebase_admin.initialize_app(cred)


class FirebaseAuthentication(authentication.BaseAuthentication):
    
    def authenticate(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION")
        is_testing = request.GET.get("is_testing", False)
        if is_testing:
            uid = "aftabuid" # user for devl
            try:
                user = CustomUser.objects.get(uid=uid)
                user.last_login = timezone.localtime()
            except Exception:
                raise InvalidAuthToken("Please register this token first @ /api/v1/accounts/user/register/")
            
            return (user, uid)

        if not auth_header:
            raise NoAuthToken("No auth token provided")

        id_token = auth_header.split(" ").pop()
        decoded_token = None

        try:
            decoded_token = auth.verify_id_token(id_token)            
        except Exception:
            raise InvalidAuthToken("Invalid/expired auth token")

        if not id_token or not decoded_token:
            return None

        try:
            uid = decoded_token.get("uid")
        except Exception:
            raise FirebaseError()
        
        try:
            user = CustomUser.objects.get(uid=uid)
            user.last_login = timezone.localtime()
        except Exception:
            raise InvalidAuthToken("Please register this token first @ /api/v1/accounts/user/register/")
        return (user, uid)

   

    def get_uid_from_token(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION")
        uid = auth_header.split(" ").pop()
        decoded_token = auth.verify_id_token(uid)
        uid = decoded_token.get('uid')
        return uid  
     
    def get_user_from_token(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION")
        uid = auth_header.split(" ").pop()
        decoded_token = auth.verify_id_token(uid)
        uid = decoded_token.get('uid')
        try:
            user = CustomUser.objects.get(uid=uid)
        except:
            raise InvalidAuthToken("Please register this token first @ /api/v1/accounts/user/register/")

        return user 
      
    def get_user_from_auth_token(self, auth_token):
        uid = auth_token.split(" ").pop()
        decoded_token = auth.verify_id_token(uid)
        uid = decoded_token.get('uid')
        print(uid)
        # uid = "3O7tSphxWRVUpwIjgC8hhWZnPXD3"
        try:
            user = CustomUser.objects.get(uid=uid)
        except:
            raise InvalidAuthToken("Please register this token first @ /api/v1/accounts/user/register/")

        return user   

    
    def get_firebase_user(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION") 
        # testing purpose
        if request.GET.get("is_testing", False):
            return auth.get_user(uid="DLxv8hBWgtUopvaowPyA6ep7rOR2") 

        if not auth_header:
            raise NoAuthToken("No auth token provided")
        
        id_token = auth_header.split(" ").pop()
        decoded_token = None

        try:
            decoded_token = auth.verify_id_token(id_token)            
        except Exception:
            raise InvalidAuthToken("Invalid/expired auth token")

        try:
            uid = decoded_token.get("uid")
        except Exception:
            raise FirebaseError()
       
        return auth.get_user(uid=uid) 
    

def send_notification_to_multiple(title: str, body: str, data, tokens):
   
    alert = messaging.ApsAlert(title = title, body = body)
    aps = messaging.Aps(custom_data=data, alert=alert)
    payload = messaging.APNSPayload(aps)
    print("payload", payload)
    # notification = messaging.Notification(title="hello", body="hi")
    message = messaging.MulticastMessage(
                        data=data,
                        apns=messaging.APNSConfig(payload=payload),
                        tokens=tokens 
                        )
    
    response = messaging.send_multicast(message)
    print(response)
    if response.failure_count > 0:
        responses = response.responses
        print(responses)
        print(responses)
        failed_tokens = []
        for idx, resp in enumerate(responses):
            print(resp.__dict__)
            if not resp.success:
                # The order of responses corresponds to the order of the registration tokens.
                failed_tokens.append(tokens[idx])
        print('List of tokens that caused failures: {0}'.format(failed_tokens))
        
    return response
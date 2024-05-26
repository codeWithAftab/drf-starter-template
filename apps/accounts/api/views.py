from rest_framework import serializers
from .serializers import UserSerializer
from rest_framework.views import APIView
from apps.accounts.models import CustomUser
from rest_framework.response import Response
from exceptions.restapi import CustomAPIException
from apps.accounts.services import CustomUserManager
from authentication.firebase import FirebaseAuthentication


class RegisterApi_v3(APIView):
    class InputSerializer(serializers.ModelSerializer):
        device_id = serializers.CharField(required=True)
        
        class Meta:
            model = CustomUser
            fields = [ 
                       "phone_number", 
                       "device_id", 
                       "first_name", 
                       "last_name", 
                       'gender', 
                       "image",
                        'cover_image',
                        'first_name',
                        'last_name',
                        'phone_number',
                        'weight',
                        'height',
                        'gender',
                        'address_line',
                        'zip_code',
                        'country',
                        'country_code',
                        'date_of_birth',
                        'is_partner',
                      ]
        
    def _get_firebase_user(self, request):
        fra = FirebaseAuthentication()
        return fra.get_firebase_user(request=request)

    def post(self, request, *args,  **kwargs):
        firebase_user = self._get_firebase_user(request=request)
        print(firebase_user.uid)
        serializer = self.InputSerializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            raise CustomAPIException(detail=str(e), error_code="MissingFieldError")
        
        user_manager = CustomUserManager(uid=firebase_user.uid)
        
        if not firebase_user.provider_data:
            user = user_manager.create_guest_user(firebase_user, **serializer.data)
            return Response({"data": UserSerializer(user).data})

        user = user_manager.create_user(firebase_user, **serializer.data)
        return Response({"data": UserSerializer(user).data})
        
        
    def patch(self, request, *args,  **kwargs):
        firebase_user = self._get_firebase_user(request=request)
        user_manager = UserSerializer(uid=firebase_user.uid)
        user = user_manager.update_user(**request.data)
        return Response({"data": UserSerializer(user).data})

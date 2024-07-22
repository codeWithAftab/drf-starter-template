# standard imports.
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

# third part imports.
from rest_framework_simplejwt.authentication import JWTAuthentication

# local imports
from .serializers import UserSerializer, StaffMemberSerializer
from exceptions.restapi import CustomAPIException
from apps.accounts.services import *
from apps.accounts.services import create_user, update_user


class RegisterAPI(APIView):
    class InputSerializer(serializers.Serializer):
        first_name = serializers.CharField( max_length=20 )
        last_name = serializers.CharField( max_length=20, required=False )
        image = serializers.ImageField( required=False )
        email = serializers.EmailField( required=True )
        password = serializers.CharField( required=True )
        role = serializers.ChoiceField( choices=USER_ROLES, default="manager" )

    def post(self, request, *args,  **kwargs):
        serializer = self.InputSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            raise CustomAPIException(detail=str(e), error_code="MissingFieldError")
   
        user = create_user( **serializer.validated_data )
        return Response({"data": UserSerializer(user, context={"request":request}).data})

class UpdateUserAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    class InputSerializer(serializers.Serializer):
        first_name = serializers.CharField( max_length=20, required=False )
        last_name = serializers.CharField( max_length=20, required=False )
        image = serializers.ImageField( required=False )
        role = serializers.ChoiceField( choices=USER_ROLES, required=False )

    def patch(self, request, *args,  **kwargs):
        serializer = self.InputSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            raise CustomAPIException(detail=str(e), error_code="MissingFieldError")
   
        user = update_user(user=request.user, **serializer.validated_data)
        return Response({"data": UserSerializer(user, context={"request":request}).data})


class UserProfileAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user, context={"request":request})
        response = {
            "status":200,
            "data":serializer.data
        }
        return Response(data=response, status=status.HTTP_200_OK)
    

class AddNewStaffMemberAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    class InputSerializer(serializers.Serializer):
        first_name = serializers.CharField( max_length=20 )
        last_name = serializers.CharField( max_length=20, required=False )
        image = serializers.ImageField( required=False )
        email = serializers.EmailField( required=True )
        password = serializers.CharField( required=True )
    
    def post(self, request, *args,  **kwargs):
        serializer = self.InputSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            raise CustomAPIException(detail=str(e), error_code="MissingFieldError")
        
        user = create_staff_member(manager=request.user, **serializer.validated_data)
        return Response({"data": StaffMemberSerializer(user, context={"request":request}).data})
    

class GetStaffMembersDetailAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


    def get(self, request, *args,  **kwargs):
        staff_members = get_all_staff_members(manager=request.user)
        output_serializer = StaffMemberSerializer(staff_members, many=True, context={"request":request})
        response = {
            "count": len(output_serializer.data),
            "data": output_serializer.data
        }
        return Response(response)
    

class UpdateStaffMemberDetailsAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    class InputSerializer(serializers.Serializer):
        employee_id = serializers.CharField( max_length=20 )
        first_name = serializers.CharField( max_length=20 )
        last_name = serializers.CharField( max_length=20, required=False )
        image = serializers.ImageField( required=False )
       
    def patch(self, request, *args,  **kwargs):
        serializer = self.InputSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            raise CustomAPIException(detail=str(e), error_code="MissingFieldError")
        
        user = update_staff_member_details(manager=request.user, **serializer.validated_data)
        output_serializer = StaffMemberSerializer(user, context={"request":request})
        response = {
            "data": output_serializer.data
        }
        return Response(response)
  
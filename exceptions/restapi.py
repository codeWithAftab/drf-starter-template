from rest_framework import status
from rest_framework.exceptions import APIException
from apps.core.models import CustomErrors
from rest_framework import serializers
from rest_framework.views import exception_handler
from rest_framework.response import Response


class ErrorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomErrors
        fields = "__all__"

def custom_exception_handler(exc, context):
    # Call the default exception handler first  
    response = exception_handler(exc, context)
    print("error response", response)
    if response is not None:
        error_field = exc.__dict__.get("error")
        print(exc.__dict__)
        if error_field:
            if not exc.detail:
                response.data = exc.error
            else:
                response.data = exc.error
                response.data["detail"] = exc.detail

    return response


class CustomAPIException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = None
    default_code = None

    def __init__(self, detail=None, code=None, error_code=None):
        super().__init__(detail, code)
        try:
            self.detail = detail
            print("detail", detail)
            error = CustomErrors.objects.get(code=error_code)
            print(error)
            self.status_code = error.status_code
            serializer = ErrorSerializer(error)
            print(serializer.data)
            self.error = serializer.data

            
        except Exception as e:
            print("exception ", e)
            self.error = None






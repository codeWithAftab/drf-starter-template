from rest_framework import serializers
from helper.constant import USER_ROLES

class UserSerializer(serializers.Serializer):
    uuid = serializers.CharField(read_only=True)
    first_name = serializers.CharField(allow_blank=True, required=False, max_length=20)
    last_name = serializers.CharField(allow_blank=True, required=False, max_length=20)
    image = serializers.ImageField(allow_null=True, required=False)
    email = serializers.EmailField(required=True)
    role = serializers.ChoiceField(choices=USER_ROLES, required=True)
    created_on = serializers.DateTimeField(read_only=True)
    updated_on = serializers.DateTimeField(read_only=True)

    def get_image(self, obj):
        try:
            request = self.context["request"]
            return request.build_absolute_uri(obj.image.url)
        
        except:
            return None
    

class StaffMemberSerializer(serializers.Serializer):
    user = UserSerializer()
    employee_id = serializers.CharField()
    weekly_off = serializers.JSONField()
 
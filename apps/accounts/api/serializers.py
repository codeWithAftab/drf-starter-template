from rest_framework import serializers

class UserSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.CharField()
    phone_number = serializers.CharField()
    date_of_birth = serializers.DateField()
    zip_code = serializers.IntegerField()



# class CustomRegisterSerializer_v2(serializers.ModelSerializer):
#     last_name = serializers.CharField()
#     last_name = serializers.CharField()
#     email = serializers.SerializerMethodField()
#     subscription = serializers.SerializerMethodField()
#     local_masjid = serializers.SerializerMethodField()
#     prefrences = serializers.SerializerMethodField()
#     admin_of_masjid = serializers.SerializerMethodField()

#     class Meta:
#         model = CustomUser
#         fields = (
#                   'uid', "uuid", 'username', 'email', 'is_email_verified', 
#                   'firebase_token','first_name', 'last_name', 'phone_number',
#                   "is_masjid_admin", "prefrences", 
#                   'country_code','zip_code', 'country', 'subscription','date_of_birth',
#                   "local_masjid", "admin_of_masjid", 'created_on', 'updated_on'
#                   )

#     def get_local_masjid(self, obj):
#         try:
#             masjid = obj.local_masjid
#             if masjid:
#                 return MasjidSerializerV3(masjid).data
      
#         except Exception as e:
#             print(e)

#         return None
    
#     def get_prefrences(self, obj: CustomUser):
#         prefrences = obj.prefrences.all()
#         if not prefrences:
#             return None

#         serializer = SubCategorySerializer(prefrences, many=True)
#         return serializer.data
        
    
#     def get_admin_of_masjid(self, obj: CustomUser):
#         try:
#             if obj.is_masjid_admin:
#                 return MasjidSerializerV3(obj.get_masjid()).data
        
        
#         except Exception as e:
#             print(e)

#         return None
    
#     def get_email(self, obj):
#         email = obj.email
#         print(email)
#         if "@placeholder.com" in email:
#             return None
#         return email
    

    
#     def get_subscription(self, user):
#         if not user or not user.is_premium:
#             return None
        
#         try:
#             subscription = UserPremiumSubscription.objects.get(user=user)
#             serializer = UserPremiumSubscriptionSerializer(subscription)
#             return serializer.data
        
#         except Exception as e:
#             return None
        
        
#     def _add_fcm_token(self, user, data):
#         device_id = data.get("device_id", None)
#         fcm_token = data.get("fcm_token", None)
#         # device and fcm token store.
#         try:
#             device = Device.objects.get(user=user, device_id=device_id)
#             device.fcm_token = fcm_token
#             device.save()
#             return device
        
#         except Device.DoesNotExist:
#             device = Device.objects.create(user=user, device_id=device_id, fcm_token=fcm_token)
#             return device

#     def save(self, request):
#         user = CustomUser.objects.get(uid=request.data["uid"])
#         user.first_name = request.data.get("first_name")
#         user.last_name = request.data.get("last_name")
#         user.email = request.data.get("email")
#         user.address_line_1 = request.data.get("address_line_1")
#         user.address_line_2 = request.data.get("address_line_2")
#         user.firebase_token = request.data.get("firebase_token")
#         user.zip_code = request.data.get("zip_code")
#         user.date_of_birth = request.data.get("date_of_birth")
#         user.save()
        
#         if request.data.get("device_id"):
#             data = request.data
#             self._add_fcm_token(user,data)
      
#         return user
    
#     def partial_update(self, request):
#         user = CustomUser.objects.get(uid=request.data["uid"])
#         user.first_name = request.data.get("first_name",user.first_name)
#         user.last_name = request.data.get("last_name",user.last_name)
#         user.email = request.data.get("email",user.email)
#         user.is_email_verified = request.data.get("is_email_verified",user.is_email_verified)
#         user.address_line_1 = request.data.get("address_line_1",user.address_line_1)
#         user.address_line_2 = request.data.get("address_line_2",user.address_line_2)
#         user.firebase_token = request.data.get("firebase_token",user.firebase_token)
#         user.zip_code = request.data.get("zip_code",user.zip_code)
#         user.date_of_birth = request.data.get("date_of_birth",user.date_of_birth)
#         user.save()
        
#         if request.data.get("device_id"):
#             data = request.data
#             self._add_fcm_token(user,data)

#         return user
    

#     # class CustomRegisterSerializer(serializers.ModelSerializer):
#     # last_name = serializers.CharField()

#     # class Meta:
#     #     model = CustomUser
#     #     fields = "__all__"

#     # def update_user_fields(self, user, data):
#     #     user.first_name = data.get("first_name", user.first_name)
#     #     user.last_name = data.get("last_name", user.last_name)
#     #     user.email = data.get("email", user.email)
#     #     user.address_line_1 = data.get("address_line_1", user.address_line_1)
#     #     user.address_line_2 = data.get("address_line_2", user.address_line_2)
#     #     user.firebase_token = data.get("firebase_token", user.firebase_token)
#     #     user.zip_code = data.get("zip_code", user.zip_code)
#     #     user.date_of_birth = data.get("date_of_birth", user.date_of_birth)
#     #     user.save()

#     # def save(self, request):
#     #     fra = FirebaseRegisterAuthentication()
#     #     uid = fra.get_uid_from_token(request)
#     #     data = request.data

#     #     user = CustomUser.objects.get(uid=uid)
#     #     self.update_user_fields(user, data)

#     #     device_id = data.get("device_id")
#     #     fcm_token = data.get("fcm_token")
#     #     DeviceToken.objects.create(user=user, device_id=device_id, fcm_token=fcm_token)

#     #     return user
    
#     # def partial_update(self, request):
#     #     fra = FirebaseRegisterAuthentication()
#     #     uid = fra.get_uid_from_token(request)
#     #     data = request.data

#     #     user = CustomUser.objects.get(uid=uid)
#     #     self.update_user_fields(user, data)

#     #     return user

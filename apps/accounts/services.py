from .models import *
from exceptions.restapi import CustomAPIException
from firebase_admin.auth import UserRecord

class CustomUserManager:
    def __init__(self, uid=None):
        self.uid = uid
        
    def create_user(self, firebase_user: UserRecord, **validated_data):
        if not firebase_user.email:
            email = f"{self.uid}@placeholder.com"
        else:
            email = firebase_user.email

        try:
            user = CustomUser.objects.create(uid=firebase_user.uid,
                                             phone_number=firebase_user.phone_number,
                                                email=email
                                             )
        except Exception as e:
            print("error")
            raise CustomAPIException(error_code="UserAlreadyExist")
        
        return self.update_user(**validated_data)

    def create_guest_user(self, **validated_data):                                                                       
        email = f"{self.uid}-guest@placeholder.com"
        device_id = validated_data["device_id"]
        try:
            user = CustomUser.objects.create(uid=self.uid, is_guest=True, email=email)
        except Exception as e:
            raise CustomAPIException(detail=str(e), error_code="UserAlreadyExist")
    
        if self._is_device_valid_for_guest_user(device_id=device_id):
            self._add_user_to_device(user=user, device_id=device_id)
            
        else:
            raise CustomAPIException(error_code="GuestUserLoginLimitExceed")

        return user
       
    def update_user(self, **update_fields):
        user = CustomUser.objects.get(uid=self.uid)
        print(update_fields)
        for field , value in update_fields.items():
            if field != "id" and  value != "":
                setattr(user, field, value)

        print(update_fields)
        user.save()

      
        device_id = update_fields.get("device_id")
        if device_id:
            fcm_token = update_fields.get("fcm_token")
            self._add_user_to_device(user=user, device_id=device_id, fcm_token=fcm_token)

        return user

    def device_eligible_for_guest_user(self, device_id, **kwargs):
        """This method is return True if the device is valid for Guest user.
            Other wise False
        Keyword device_id:
        argument -- description
        Return: Return True if valid device.
        """
        
        if self._is_device_valid_for_guest_user(device_id=device_id):
            return True
        
        return False        
    
    def _add_device(self, user, device_id, fcm_token=None):
        try:
            device = Device.objects.get(device_id=device_id)
            device.user = user
            fcm_token = fcm_token
            device.save()
            return device

        except:
            return Device.objects.create(device_id=device_id, user=user, fcm_token=fcm_token)
        
    def _add_user_to_device(self, user, device_id, fcm_token=None):
        try:
            device = Device.objects.get(device_id=device_id)
            device.users.add(user)
            device.fcm_token = fcm_token
            device.save()
            return device

        except:
            device = Device.objects.create(device_id=device_id, fcm_token=fcm_token)
            if not user in device.users.all():
                device.users.add(user)
                
            return device

    def _is_device_valid_for_guest_user(self, device_id):
        device = Device.objects.filter(device_id=device_id).first()
        if device:
            device_creation_time = device.created_on  # Assuming this is timezone-aware
            current_time = timezone.now()  # Get the current time in the same timezone
            time_in_72_hours = device_creation_time + timedelta(hours=72)

            if time_in_72_hours > current_time:
                return True
            
            else:
                return False
        
        # if device not exist then simply create device
        return True

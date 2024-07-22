# local modules.
from .models import *
from exceptions.restapi import CustomAPIException
from .queries import *
from apps.accounts.decorators import manager_role_required

def create_user(*, email: str, password: str, **validated_data) -> CustomUser:
    """
    Create a new user with the given email and password.

    Args:
        email (str): The email address of the new user.
        password (str): The password for the new user.
        **validated_data: Additional validated data to create the user.

    Returns:
        CustomUser: The newly created user object.

    Raises:
        CustomAPIException: If a user with the given email already exists.
    """
    user = get_user_by_email(email=email)

    if user:
        raise CustomAPIException( error_code="EmailAlreadyExist")

    user = CustomUser.objects.create(email=email, **validated_data)
    user.set_password(password)
    user.save()

    return user


def update_user(*, user: CustomUser, **validated_data) -> CustomUser:
    """
    Update an existing user with the given validated data.

    Args:
        user (CustomUser): The user object to update.
        **validated_data: The fields and values to update the user with.

    Returns:
        CustomUser: The updated user object.

    Raises:
        None
    """
    for field, value in validated_data.items():
        setattr(user, field, value)

    user.save()

    return user


@manager_role_required
def create_staff_member(*,
                        manager: CustomUser,
                        email: str,
                        password: str,
                        role: str = "staff",
                        **validated_data) -> StaffMember:
    """
    Create a new staff member by a user with the manager role.

    Args:
        manager (CustomUser): The manager creating the staff member.
        email (str): The email address of the new staff member.
        password (str): The password for the new staff member.
        role (int): The role of the new staff member, default is 1 (Staff).
        employee_id (str): The employee ID of the new staff member.
        **validated_data: Additional validated data to create the user.

    Returns:
        StaffMember: The newly created staff member object.

    Raises:
        CustomAPIException: If a user with the given email already exists.
    """
    user = create_user(email=email, password=password, role=role, **validated_data)
    staff_member = StaffMember(user=user)
    staff_member.save()

    return staff_member

@manager_role_required
def update_staff_member_details(*, 
                                manager: CustomUser, 
                                employee_id: str,
                                **validated_data) -> CustomUser:
    staff_member = get_staff_member_by_id(employee_id=employee_id)
    if not staff_member:
        raise CustomAPIException(error_code="WrongEmployeeId")
    
    for field, value in validated_data.items():
        setattr(staff_member.user, field, value)

    staff_member.user.save()

    return staff_member


@manager_role_required
def get_all_staff_members(manager: CustomUser):
    staff_members = StaffMember.objects.all()
    return staff_members

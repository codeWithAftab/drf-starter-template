from apps.accounts.models import CustomUser, StaffManager, StaffMember
from exceptions.auth import UserNotFound
from typing import Optional, Literal


def get_user_by_email(*, email: str) -> CustomUser:
    """
    Retrieve a user by their email address.

    Args:
        email (str): The email address of the user to retrieve.

    Returns:
        CustomUser: The user object corresponding to the given email address.
        None: If no user with the given email address exists.

    Raises:
        None
    """
    try:
        user = CustomUser.objects.get(email=email)
        return user
    except CustomUser.DoesNotExist:
        return None


def get_staff_member_by_id(employee_id: str) -> Optional[StaffMember]:
    """
    Retrieves a staff member by their employee ID.

    Args:
        employee_id (str): The ID of the employee to retrieve.

    Returns:
        Optional[StaffMember]: The staff member if found, otherwise None.
    """
    try:
        staff = StaffMember.objects.get(employee_id=employee_id)
        return staff
    except StaffMember.DoesNotExist:
        return None
    
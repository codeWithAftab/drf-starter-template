"""
decorators.py

This module contains decorators used to enforce role-based access control in the attendance management system.
These decorators ensure that only users with the appropriate roles can access certain functionalities.

Functions:

- manager_role_required(fx):
    Ensures that the user has the manager role before allowing access to the decorated function.

- staff_member_role_required(fx):
    Ensures that the user has the staff member role before allowing access to the decorated function.
"""

from exceptions.restapi import CustomAPIException

def manager_role_required(fx):
    """
    Decorator to ensure the user has the manager role.

    Args:
        fx (function): The function to be decorated.

    Returns:
        function: The decorated function with role-based access control.
    
    Raises:
        CustomAPIException: If the user does not have the manager role.
    """
    def mfx(*args, **kwargs):
        user = kwargs.get("manager")
        print(user.role)
        if user.role != "manager":
            raise CustomAPIException(detail="PermissionError", error_code="PermissionError")
        
        return fx(*args, **kwargs)
    
    return mfx

def staff_member_role_required(fx):
    """
    Decorator to ensure the user has the staff member role.

    Args:
        fx (function): The function to be decorated.

    Returns:
        function: The decorated function with role-based access control.
    
    Raises:
        CustomAPIException: If the user does not have the staff member role.
    """
    def mfx(*args, **kwargs):
        user = kwargs.get("staff_user")
        print(user.role)
        if user.role != "staff":
            raise CustomAPIException(detail="User role should be the 'staff member' to perform this action.", error_code="PermissionError")
        
        return fx(*args, **kwargs)
    
    return mfx

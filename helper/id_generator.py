import uuid

def generate_employee_id():
    return  f"emp_{str(uuid.uuid4().hex)[:6]}"  
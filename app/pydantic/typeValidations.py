from pydantic import BaseModel
from typing import Optional


# Pydantic Type Validations................
class Patient(BaseModel):
    name: str
    age: int
    email: Optional[str] = None  # Optional field with default value None

patient_data = {'name': '65', 'age': 32}
patient1 = Patient(**patient_data)

def print_data(data: Patient):
    print(data.name)
    print(data.age)
    print(data.email)

 
print_data(patient1)
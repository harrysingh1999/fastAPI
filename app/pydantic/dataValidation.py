from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator, model_validator
from typing import Optional

# Pydantic provides built in methods and proerties for generic and custom data validation......................

class Patient(BaseModel):
    name: str
    email: EmailStr
    number: int
    age: int = Field(gt=4, lt=50, strict=True) # Strict ensures that the value should be strictly of defined type, not coercible or automatically converted intelligently by Pydantic.....................
    linkedin: AnyUrl

patient_data = {'name': '65', 'email': '65@example.com', 'number': '8393839393', 'age': 32, 'linkedin': 'https://www.linkedin.com'}
patient1 = Patient(**patient_data)

def print_data(data: Patient):
    print(data.name)
    print(data.email)
    print(data.age)
    print(data.linkedin)

# print_data(patient1)


# Field Validator is used to apply custom validation in a single field at a time.................

class Patient2 (BaseModel):
    name: str
    email: EmailStr
    age: int
    weight: float
    married: bool
    allergies: Optional[list[str]]
    contact_details: Optional[dict[str, str]]

    @field_validator('email')
    @classmethod
    def email_validator(cls, value):
        valid_domains = ['hdfc.com', 'icici.com']
        domain = value.split('@')[-1]
        print(value)
        if domain not in valid_domains:
            raise ValueError(f"Email domain must be one of {valid_domains}")
        return value

patient_data2 = {'name': '65', 'email': '65@hdfc.com', 'age': 32, 'weight': 70.5,
                 'married': True, 'allergies': ['pollen', 'dust'],
                   'contact_details': {'phone': '1234567890', 'address': '123 Main St'}}
patient2 = Patient2(**patient_data2)

def print_data2(data: Patient2):
    print(data.name)
    print(data.email)
    print(data.age)
    print(data.weight)
    print(data.married)
    print(data.allergies)
    print(data.contact_details)

# print_data2(patient2)

# Model Validator is used to apply custom validations on multiple fields at a time.................

class Patient3 (BaseModel):
    name: str
    email: EmailStr
    age: int
  
    @model_validator(mode='after') # here mode is mandatory, when after it means values will be available after the type coercion...........
    def email_validator(cls, model):
       if model.age > 60 and 'emergency' not in model.contact_details:
           raise ValueError("Emergency contact details are required for patients over 60.")
       return model

patient_data3 = {'name': '65', 'email': '65@hdfc.com', 'age': 7}
patient3 = Patient3(**patient_data3)
print('Patient 3 data:', patient3.name)

def print_data2(data: Patient3):
    print(data.name)
    print(data.email)
    print(data.age)

print_data2(patient3)
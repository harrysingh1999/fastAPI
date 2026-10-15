from pydantic import BaseModel


# Pydantic Type and Data Validations................
# Pydantic provides built in methods and proerties for generic and custom data validation......................

class Patient(BaseModel):
    name: str
    age: int

patient_data = {'name': '65', 'age': 32}
patient1 = Patient(**patient_data)

def print_data(data: Patient):
    print(data.name)
    print(data.age)

 
print_data(patient1)
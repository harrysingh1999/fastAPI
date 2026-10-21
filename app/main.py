import json

from app.pydantic.api_pydantic_models import Patient
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse

app = FastAPI()

def load_data():
    with open('app\patients.json', 'r') as f:
        data = json.load(f)
    return data

def save_data(data):
    with open('app\patients.json', 'w') as f:
        json.dump(data, f)

@app.get("/")
def root():
    return 'Welcome to Fast API'


@app.get("/patients")
def get_patients():
    data = load_data()
    return data

@app.get("/patients/{patient_id}")
def get_patient(patient_id: str):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(
        status_code=404, detail=f'this {patient_id}, Patient not found')


@app.get("/sort")
def sort_patients(sort_by: str = Query(..., description='Sort on the basis of height, weight or BMI'), #... means that parameter is required..........
                  order: str = Query('desc', description='Sort in asc or desc order')):

    valid_fields = ['height', 'weight', 'bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f'Invalid field select, it should be from {valid_fields}')
    
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail='Invalid Order Selection, must be asc or desc')

    data = load_data()
    sort_order = True if order == 'desc' else False
    sorted_data = sorted(data.values(), key=lambda x: x.get(
    sort_by, 0), reverse=sort_order)

    return sorted_data

@app.post('/create')
def create_patient(patient: Patient):
    # load existing data
    data = load_data()

    # check if the patient already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail='Patient already exists')

    # new patient add to the database
    data[patient.id] = patient.model_dump(exclude=['id'])

    # save the created data.........
    save_data(data)
    
    return JSONResponse(status_code=201, content={'message': 'Patient Created Successfully' })
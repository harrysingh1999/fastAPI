import json


from fastapi import FastAPI, HTTPException, Query

app = FastAPI()


def load_data():
    with open('app\patients.json', 'r') as g:
        data = json.load(g)
    return data


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
def sort_patients(sort_by: str = Query(..., description='Sort on the basis of height, weight or BMI'),
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

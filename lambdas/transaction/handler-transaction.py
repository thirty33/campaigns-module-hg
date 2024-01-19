
import os
from fastapi import FastAPI, Body, HTTPException, Path, Query, Depends, Request, security, status
from lambdas.transaction.helpers.dbClient import tableClient
from lambdas.transaction.helpers.sqsClient import sqsClient
from lambdas.transaction.authClient import authClient, get_current_user
from lambdas.transaction.helpers.models import Transaction, LoginRequest, User, ParamsModel
from mangum import Mangum
import uuid
import json
from typing import Dict
from fastapi.middleware.cors import CORSMiddleware
import resend
# from lambdas.sendEmail.helpers.template import export_html

resend.api_key = os.environ["RESEND_API_KEY"]
STAGE = os.environ.get('STAGE')
FROM_EMAIL = os.environ.get('FROM_EMAIL')
TO_EMAIL = os.environ.get('TO_EMAIL')
root_path = '/' if not STAGE else f'/{STAGE}'

app = FastAPI(
    title="Campaigns Module Api",
    debug=False,
    version="1.0.0",
    root_path=root_path
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.environ.get('FRONT_URL')],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def convert_dict_values_to_string(input_dict: Dict) -> Dict:
    for key, value in input_dict.items():
        input_dict[key] = str(value)
    return input_dict


@app.post('/information-request/create', tags=['Information Request'])
def create_custom_model(
    transaction: Transaction,
    # sub: str = Depends(get_current_user),
    # token: str = ''
):
    # Convert pydantic model to dict
    tableClient.set_table(os.environ.get('table_transaction_name'))
    transaction_dict = transaction.model_dump()

    transaction_dict = convert_dict_values_to_string(transaction_dict)

    # Add Uid to the dictionary
    transaction_dict["Uid"] = str(uuid.uuid4())

    return tableClient.put_item(item=transaction_dict)


@app.get('/information-request/list', tags=['Information Request'])
def list_custom_model(
    params: ParamsModel = Depends(),
    sub: str = Depends(get_current_user),
    token: str = ''
):
    tableClient.set_table(os.environ.get('table_transaction_name'))
    filters = params.model_dump()
    filters.pop('token', None)

    return tableClient.get_item(filters)


@app.delete('/information-request/delete/{id}', tags=['Information Request'])
def delete_custom_model(id: str, sub: str = Depends(get_current_user), token: str = ''):
    tableClient.set_table(os.environ.get('table_transaction_name'))
    return tableClient.delete_item(id)


@app.put('/information-request/update/{id}', tags=['Information Request'], response_model=dict)
def update_custom_model(
    id: str,
    transaction: Transaction,
    sub: str = Depends(get_current_user),
    token: str = ''
):
    tableClient.set_table(os.environ.get('table_transaction_name'))
    transaction_dict = transaction.model_dump()
    transaction_dict = convert_dict_values_to_string(transaction_dict)
    return tableClient.update_item(id, transaction_dict)


@app.post('/user/create', tags=['user'])
def create_user(
    login_request: LoginRequest,
):
    tableCLientResponse = {}
    data_dict = {}
    createUserResponse = authClient.admin_create_user(
        login_request.email, login_request.password)

    if createUserResponse['status_code'] and createUserResponse['status_code'] >= 200 and createUserResponse['status_code'] < 204:
        tableClient.set_table(os.environ.get('user_transaction_name'))
        tableCLientResponse = tableClient.put_item(item={
            "Email": login_request.email,
            "Password": login_request.password,
            "Uid": str(uuid.uuid4())
        })
        json_content = tableCLientResponse.body.decode()
        data_dict = json.loads(json_content)

    data = {
        'create-user-cognito': json.loads(json.dumps(createUserResponse, default=authClient.serialize_datetime)),
        'create-user-dynamo': data_dict
    }
    return tableClient.manage_sucessfull_response(data, 201)


@app.get('/user/login', tags=['user'])
def login_user(
    login_request: LoginRequest = Depends()
):
    print('response one')
    response = authClient.admin_initiate_auth(
        login_request.email, login_request.password)
    print('response two')
    return tableClient.manage_sucessfull_response(response)
    # print('test', os.environ.get('user_transaction_name'))
    # tableClient.set_table(os.environ.get('user_transaction_name'))

    # return tableClient.get_single_model({
    #     "Email": email,
    #     "Uid": uid
    # })


# @app.post('/test-message/send', tags=['message'])
# def send_message(
#     sub: str = Depends(get_current_user),
#     token: str = ''
# ):
#     try:
#         body_string = '{\n  "Title": "quote",\n  "Category": "1",\n  "Bank": "1",\n  "DateTransaction": "2023-01-01 10:30:50",\n  "Description": "Description",\n  "nombreApellido": "dasd",\n  "email": "test@test.com",\n  "genero": "masculino",\n  "Telefono": "+51",\n  "numeroTelefonico": "213123122",\n  "ciudadOrigen": "dsads",\n  "ciudadDestino": "dasdsa",\n  "tipoViaje": "Viaje de ida",\n  "fechaSalida": "2023-01-01 10:30:50",\n  "fechaRegreso": "2023-02-27 20:30:50",\n  "optionViaje": "Plan completo (vuelos, hotel y tours)",\n  "recibirCotizacion": "WhatsApp",\n  "amountPersons": "1",\n  "Uid": "179320c2-7b3b-4195-aaed-a6ef32e2033b"\n}'
#         object_element = json.loads(body_string)

#         responseEmail = resend.Emails.send({
#             "from": FROM_EMAIL,
#             "to": TO_EMAIL,
#             "subject": "Información sobre cotización",
#             "html": export_html(object_element)
#         })

#         print('responseEmail', responseEmail)

#         return True
#     except:
#         return False
    
handler = Mangum(app)

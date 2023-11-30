
import os
from fastapi import FastAPI, Body, HTTPException, Path, Query, Depends, Request, security, status
from lambdas.transaction.helpers.dbClient import tableClient
from lambdas.transaction.authClient import authClient, get_current_user
from lambdas.transaction.helpers.models import Transaction, LoginRequest, User, ParamsModel
from mangum import Mangum
import uuid
import json
from typing import Dict
from fastapi.middleware.cors import CORSMiddleware

STAGE = os.environ.get('STAGE')
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


handler = Mangum(app)

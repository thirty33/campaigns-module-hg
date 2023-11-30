
import boto3
import json
from botocore.exceptions import ClientError
import decimal
import os
from fastapi.responses import HTMLResponse, JSONResponse
from boto3.dynamodb.conditions import Attr


class SingletonMeta(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class TableClient(metaclass=SingletonMeta):

    # def __init__(self):
    def instance(self):

        self.exclusiveStartKey = {}
        self.client = boto3.resource('dynamodb')

        IS_OFFLINE = os.getenv('IS_OFFLINE', False)
        if IS_OFFLINE:
            boto3.Session(
                aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
                aws_session_token=os.environ['AWS_SESSION_TOKEN']
            )
            self.client = boto3.resource(
                'dynamodb', endpoint_url='http://localhost:8000')

        self.table = self.client.Table(
            os.environ.get('table_transaction_name'))

    def set_table(self, table):
        self.table = self.client.Table(table)

    def manage_sucessfull_response(self, response, status_code=201):
        return JSONResponse(
            content={
                'error': 'false',
                'data': response
            },
            status_code=status_code
        )

    def manage_failed_response(self, err):
        return JSONResponse(
            content={
                'error': 'true',
                'response': err.response['Error']['Message'],
            },
            status_code=500
        )

    def put_item(self, item):
        try:
            query_params = {
                'Item': item,
                # 'ReturnValues': 'ALL_NEW'
            }
            response = self.table.put_item(**query_params)
            print('put_item', json.dumps(response, indent=2))
            # return self.manage_sucessfull_response(response)
            return self.manage_sucessfull_response(item)
        except ClientError as err:
            return self.manage_failed_response(err)

    def decimal_default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)  # Convierte el Decimal en una cadena
        raise TypeError

    def get_item(self, filtersObject):
        try:

            query_params_set = {}
            filter_expressions = []
            attribute_values = {}
            for key in filtersObject.keys():
                if filtersObject[key] is not None:
                    if key != 'Title' and key != 'DateTransaction' and key != 'page' and key != 'Uid':
                        filter_expressions.append(f"{key} = :{key}")
                    if key != 'DateTransaction' and key != 'page'  and key != 'Uid':
                        attribute_values[f":{key}"] = filtersObject[key]

            query_params_set["FilterExpression"] = " AND ".join(filter_expressions)
            query_params_set["ExpressionAttributeValues"] = attribute_values

            projection_keys = [key for key in filtersObject.keys() if key != 'page']
            if 'Uid' not in projection_keys:
                projection_keys.append('Uid')
            
            query_params = {
                'IndexName': 'DateIndex',
                'KeyConditionExpression': 'Title = :Title',
                'FilterExpression': query_params_set["FilterExpression"],
                'ExpressionAttributeValues': query_params_set["ExpressionAttributeValues"],
                'ScanIndexForward': False,
                'ProjectionExpression': ", ".join(projection_keys),
                'Limit': 5,  # Cantidad de elementos por página
            }

            print('query_params_test', query_params)

            if filtersObject['page'] != '1':
                self.exclusiveStartKey = {
                    "DateTransaction": filtersObject['DateTransaction'],
                    "Title": filtersObject['Title'],
                    "Uid": filtersObject['Uid'],
                }

                print('self.exclusiveStartKey', self.exclusiveStartKey)
                if self.exclusiveStartKey:
                  query_params['ExclusiveStartKey'] = self.exclusiveStartKey

            response = self.table.query(**query_params)

            print('response', response)

            print('LastEvaluatedKey', response.get('LastEvaluatedKey', ''))

            result = {
                'Items': json.loads(json.dumps(response.get('Items', []), default=self.decimal_default)),
            }

            return self.manage_sucessfull_response(result)

        except ClientError as err:
            return self.manage_failed_response(err)

    def delete_item(self, id):

        try:
            query_params = {
                'Key': {
                    'Title': 'transaction',
                    'Uid': id,
                },
            }
            response = self.table.delete_item(**query_params)
            return self.manage_sucessfull_response(response)
        except ClientError as err:
            return self.manage_failed_response(err)

    def create_expressions(self, model):
        # Inicializar las expresiones
        update_expression = 'SET '
        expression_attribute_names = {}
        expression_attribute_values = {}

        # Recorrer el diccionario y construir las expresiones
        for key, value in model.items():
            if key != 'Title':
                # Generar un nombre de atributo de expresión único
                attribute_name = f'#{key}'
                expression_attribute_names[attribute_name] = key
                # Generar un nombre de valor de expresión único
                attribute_value = f':{key}'
                expression_attribute_values[attribute_value] = value
                # Agregar la parte SET a la expresión de actualización
                update_expression += f'{attribute_name} = {attribute_value}, '

        # Eliminar la coma final y espacios en blanco
        update_expression = update_expression[:-2]

        return update_expression, expression_attribute_names, expression_attribute_values

    def update_item(self, id, transaction):
        try:

            print('model', transaction)

            update_expresion, attribute_names, expression_attribute_values = self.create_expressions(
                transaction)

            query_params = {
                'Key': {
                    'Title': 'quote',
                    'Uid': id,
                },
                'UpdateExpression': update_expresion,
                'ExpressionAttributeNames': attribute_names,
                'ExpressionAttributeValues': expression_attribute_values,
            }

            print('query_params', query_params)

            response = self.table.update_item(**query_params)

            print('response', response)
            return self.manage_sucessfull_response(response, 200)

        except ClientError as err:
            return self.manage_failed_response(err)

    def get_single_model(self, model):
        try:
            print('model', model)
            query_params = {
                'Key': {
                    'Email': model['Email'],
                    'Uid': model['Uid'],
                },
                'ProjectionExpression': 'Uid'
            }
            response = self.table.get_item(**query_params)
            print('response', response)
            return self.manage_sucessfull_response(response, status_code=200)

        except ClientError as err:
            return self.manage_failed_response(err)


tableClient = TableClient()
tableClient.instance()

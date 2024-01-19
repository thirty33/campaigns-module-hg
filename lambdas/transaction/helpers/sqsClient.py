import boto3
import os
from botocore.exceptions import ClientError

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
    
class sqsClient(metaclass=SingletonMeta):

    def instance(self):

        IS_OFFLINE = os.getenv('IS_OFFLINE', False)
        if IS_OFFLINE:
            boto3.Session(
                aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
                aws_session_token=os.environ['AWS_SESSION_TOKEN']
            )

        self.client = boto3.client('sqs', region_name=os.getenv('AWS_REGION', False))

    def send_message(self, queue_url, message_body):
        try:
            self.client.send_message(
                QueueUrl=queue_url,
                MessageBody=message_body,
            )
        except ClientError as err:
            return err.response['Error']['Message']

sqsClient = sqsClient()
sqsClient.instance()
import boto3
import json
import os
import resend
from lambdas.sendEmail.helpers.template import export_html

resend.api_key = os.environ["RESEND_API_KEY"]
FROM_EMAIL = os.environ.get('FROM_EMAIL')
TO_EMAIL = os.environ.get('TO_EMAIL')

def sendEmail(event, context):

    try:
        body = event['Records'][0]['body']
        object_element = json.loads(body)

        responseEmailToAdmin = resend.Emails.send({
            "from": FROM_EMAIL,
            "to": TO_EMAIL,
            "subject": "Información sobre cotización",
            "html": export_html(object_element)
        })

        responseEmailToClient = resend.Emails.send({
            "from": FROM_EMAIL,
            "to": object_element['email'],
            "subject": "Información sobre cotización",
            "html": export_html(object_element)
        })

        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
    
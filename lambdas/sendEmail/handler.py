import boto3, json, os

def sendEmail(event, context):
    print('event', event)
    print('context', context)
import json
import boto3
import os
table_name = os.environ.get("VisitCounterTable")
dynamodb = boto3.client('dynamodb')

def lambda_handler(event, context):
    if event['httpMethod']=='GET':
        # Update the visit count in DynamoDB
        response = dynamodb.update_item(
            TableName=table_name,
            Key={'id': {'S': 'count'}},
            UpdateExpression='SET visit_count = visit_count + :incr',
            ExpressionAttributeValues={':incr': {'N': '1'}},
            ReturnValues='UPDATED_NEW'
        )
        
        # Extract and format the updated count
        updated_count = response['Attributes']['visit_count']['N']
        
        # Create a response object
        response_body = {
            'message': f'Visit count updated to {updated_count}',
            'updated_count': updated_count
        }
        
        # Return the response
        return {
            'statusCode': 200,
            'headers': {
                "X-Requested-With": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,x-requested-with",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": True,
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS, DELETE",
            },
            'body': json.dumps(response_body)
        }             
    if event['httpMethod']=='OPTIONS':
        return {
            'statusCode': 200,
            'body': "ok"
            
        }
    else:
        return {
            'statusCode': 400,
            'body': json.dumps("Unsupporte  Method "+ event['httpMethod'])
            
        }

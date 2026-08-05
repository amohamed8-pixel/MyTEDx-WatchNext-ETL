import json
import boto3
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('MyTEDx_Talks')

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return int(obj) if obj % 1 == 0 else float(obj)
        return super(DecimalEncoder, self).default(obj)

def lambda_handler(event, context):
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'GET,OPTIONS'
    }
    
    try:
        query_params = event.get('queryStringParameters') or {}
        idx_param = query_params.get('idx')
        
        if not idx_param:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'error': 'Missing parameter: idx'})
            }
        
        try:
            lookup_key = int(idx_param)
        except ValueError:
            lookup_key = idx_param

        response = table.get_item(Key={'idx': lookup_key})
        item = response.get('Item')
        
        if not item:
            return {
                'statusCode': 404,
                'headers': headers,
                'body': json.dumps({'error': 'Video not found'})
            }
            
        if 'quiz' not in item:
            item['quiz'] = [
                {
                    "question": "Qual è il tema principale affrontato in questo talk?",
                    "options": [
                        "Innovazione e Tecnologia",
                        "Sviluppo Personale e Società",
                        "Scienza e Ricerca Applicata"
                    ],
                    "correct_idx": 0
                }
            ]

        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(item, cls=DecimalEncoder)
        }

    except Exception as e:
        print(f"Error processing request: {str(e)}")
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': 'Internal server error', 'details': str(e)})
        }


   import json
import boto3
from decimal import Decimal

# Inizializzazione risorsa DynamoDB nello scope globale per ottimizzare i Cold Start
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('tedx_data')

class DecimalEncoder(json.JSONEncoder):
    """ Custom Encoder per convertire i tipi Decimal di DynamoDB in tipi nativi Python """
    def default(self, obj):
        if isinstance(obj, Decimal):
            return int(obj) if obj % 1 == 0 else float(obj)
        return super(DecimalEncoder, self).default(obj)

def lambda_handler(event, context):
    # Header CORS obbligatori per consentire le chiamate dal client Flutter
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
        'Access-Control-Allow-Methods': 'GET,OPTIONS'
    }

    # Gestione delle richieste Pre-Flight CORS (OPTIONS)
    if event.get('httpMethod') == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({'message': 'CORS enabled'})
        }

    # Estrazione del parametro video_id / idx dalla query string
    query_params = event.get('queryStringParameters') or {}
    video_id = query_params.get('video_id') or query_params.get('idx')

    # Validazione parametro obbligatorio
    if not video_id:
        return {
            'statusCode': 400,
            'headers': headers,
            'body': json.dumps({'error': 'Missing required parameter: video_id'}, cls=DecimalEncoder)
        }

    try:
        # Query GetItem su DynamoDB basata su Partition Key
        response = table.get_item(Key={'video_id': video_id})
        
        # Gestione caso Item Non Trovato (404)
        if 'Item' not in response:
            return {
                'statusCode': 404,
                'headers': headers,
                'body': json.dumps({'error': f'Video with video_id {video_id} not found'}, cls=DecimalEncoder)
            }

        item = response['Item']

        # Risposta Unificata: Metadati + Watch Next + Quiz
        payload = {
            'video_id': item.get('video_id'),
            'title': item.get('title'),
            'speaker': item.get('speaker'),
            'recommended_talks': item.get('recommended_talks', []),
            'reason': item.get('reason', 'Correlazione basata sui temi del talk'),
            'quiz': item.get('quiz', [])
        }

        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(payload, cls=DecimalEncoder)
        }

    except Exception as e:
        # Catch-all per errori server/database
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': str(e)}, cls=DecimalEncoder)
        }

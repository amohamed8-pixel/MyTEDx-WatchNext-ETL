import json
import boto3
from decimal import Decimal

# Inizializzazione risorsa DynamoDB nello scope globale per ottimizzare i Cold Start
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('tedx_data')  # Modifica con il nome esatto della tua tabella DynamoDB

class DecimalEncoder(json.JSONEncoder):
    """ Custom Encoder per convertire i tipi Decimal di DynamoDB in tipi nativi Python """
    def default(self, obj):
        if isinstance(obj, Decimal):
            return int(obj) if obj % 1 == 0 else float(obj)
        return super(DecimalEncoder, self).default(obj)

def lambda_handler(event, context):
    # Header CORS obbligatori per consentire le chiamate dall'app Flutter
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

    # Estrazione del parametro idx / video_id dalla query string
    query_params = event.get('queryStringParameters') or {}
    idx = query_params.get('idx') or query_params.get('video_id')

    # Validazione parametro obbligatorio
    if not idx:
        return {
            'statusCode': 400,
            'headers': headers,
            'body': json.dumps({'error': 'Missing required parameter: idx'}, cls=DecimalEncoder)
        }

    try:
        # Query GetItem su DynamoDB basata su Partition Key
        response = table.get_item(Key={'idx': idx})
        
        # Gestione caso Item Non Trovato (404)
        if 'Item' not in response:
            return {
                'statusCode': 404,
                'headers': headers,
                'body': json.dumps({'error': f'Video with idx {idx} not found'}, cls=DecimalEncoder)
            }

        item = response['Item']

        # Risposta Unificata: Metadati + Watch Next + Quiz
        payload = {
            'idx': item.get('idx'),
            'title': item.get('title'),
            'speaker': item.get('speaker'),
            'url': item.get('url'),
            'watch_next': item.get('watch_next', []),
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

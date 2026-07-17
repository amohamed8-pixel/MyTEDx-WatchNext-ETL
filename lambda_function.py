import json
import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    # Connessione al database DynamoDB
    dynamodb = boto3.resource('dynamodb')
    
    # Nome della tabella
    table = dynamodb.Table('MyTEDx_WatchNext_Table')

    # Estrazione dell'ID del video dalla richiesta API
    try:
        video_id = event['queryStringParameters']['idx']
    except (KeyError, TypeError):
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Missing parameter: idx'})
        }

    # Ricerca del video in DynamoDB
    try:
        response = table.get_item(Key={'video_id': video_id})
        
        # Se il video esiste, restituisce i talk consigliati
        if 'Item' in response:
            item = response['Item']
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'  
                },
                'body': json.dumps({
                    'video_id': item['video_id'],
                    'watch_next': item.get('recommended_talks', []),
                    'reason': 'Suggerito in base ai percorsi di studio degli altri utenti'
                })
            }
        else:
            # Se il video non esiste
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'Video not found'})
            }
            
    except ClientError as e:
        # Gestione degli errori di connessione AWS
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
        

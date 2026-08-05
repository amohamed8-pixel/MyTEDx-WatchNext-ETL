import json
import boto3
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('MyTEDx_WatchNext_Table')

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
        # قبول المتغير سواء بعته العميل باسم idx أو video_id
        video_id_param = query_params.get('idx') or query_params.get('video_id')
        
        if not video_id_param:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'error': 'Missing parameter: idx or video_id'})
            }

        # البحث بـ video_id كـ String مباشرة
        response = table.get_item(Key={'video_id': str(video_id_param)})
        item = response.get('Item')
        
        if not item:
            return {
                'statusCode': 404,
                'headers': headers,
                'body': json.dumps({'error': 'Video not found'})
            }
            
        # إدراج الـ Quiz لو مش موجود في الداتا
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

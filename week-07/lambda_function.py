import json, boto3
from decimal import Decimal
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Properties')
def lambda_handler(event, context):
    listing_id = event['pathParameters']['id']
    resp = table.get_item(Key={'L_ListingID': listing_id})
    return {
        'statusCode': 200,
        'body': json.dumps(
            resp.get('Item', {}),
            default=lambda x: int(x) if isinstance(x, Decimal) 
            and x == int(x) else float(x)
            )
        }

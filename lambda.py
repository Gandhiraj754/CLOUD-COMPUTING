import json
import boto3
import time

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ProductTable')

def lambda_handler(event, context):
    operation = event.get('operation')
    
    if operation == 'addProduct':
        return saveProduct(event)
    elif operation == 'listProduct':
        return getProducts()
    elif operation == 'deleteProduct':
        return deleteProduct(event)
    elif operation == 'updateProduct':
        return updateProduct(event)
    else:
        return {
            'statusCode': 400,
            'body': json.dumps('Unsupported operation')
        }

def saveProduct(event):
    gmt_time = time.gmtime()
    now = time.strftime('%a, %d %b %H:%M:%S', gmt_time)

    table.put_item(
        Item={
            'productCode': event['productCode'],
            'productName': event['productName'],
            'category': event['category'],
            'price': event['price'],
            'stock': event['stock'],
            'description': event['description'],
            'createdAt': now
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps(f"Product '{event['productName']}' (Code: {event['productCode']}) created at {now}")
    }

def getProducts():
    response = table.scan()
    items = response['Items']
    return {
        'statusCode': 200,
        'body': json.dumps(items),
        'headers': {'Content-Type': 'application/json'}
    }

def deleteProduct(event):
    table.delete_item(Key={'productCode': event['productCode']})
    return {
        'statusCode': 200,
        'body': json.dumps(f"Product {event['productCode']} deleted successfully")
    }

def updateProduct(event):
    response = table.update_item(
        Key={'productCode': event['productCode']},
        UpdateExpression="set productName=:n, category=:c, price=:p, stock=:s, description=:d",
        ExpressionAttributeValues={
            ':n': event['productName'],
            ':c': event['category'],
            ':p': event['price'],
            ':s': event['stock'],
            ':d': event['description']
        },
        ReturnValues="UPDATED_NEW"
    )
    return {
        'statusCode': 200,
        'body': json.dumps(f"Product {event['productCode']} updated successfully")
    }

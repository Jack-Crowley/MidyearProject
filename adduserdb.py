import json
import boto

def load_movies(movies, dynamodb=None):
    if not dynamodb:
        dynamodb = boto.resource('dynamodb', endpoint_url="http://localhost:8000")

    table = dynamodb.Table('Movies')
    for movie in movies:
        year = int(movie['year'])
        title = movie['title']
        print("Adding movie:", year, title)
        table.put_item(Item=movie)

dynamodb = boto.resource('dynamodb')
table = dynamodb.Table('Accounts')
print(table.creation_date_time)
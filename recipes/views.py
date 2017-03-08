from django.shortcuts import render
import boto3

def index(request):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('Recipes')
    recipes = table.scan()['Items']
    # recipes = [
    #     {'RecipeName': 'Pasta'},
    #     {'RecipeName': 'Bacon and Eggs'}
    # ]

    return render(request, 'index.html', {'recipes': recipes})

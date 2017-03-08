from django.shortcuts import render, redirect
from django.http import Http404
import boto3
from boto3.dynamodb.conditions import Key

def index(request):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('Recipes')
    recipes = table.scan()['Items']
    context = {
        'recipes': recipes,
        'body_class': 'full'
    }
    return render(request, 'index.html', context)


def view(request, recipe_name):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('Recipes')
    recipes = table.query(KeyConditionExpression=Key(
        'RecipeName').eq(recipe_name))['Items']
    if request.method == 'POST':
        table.delete_item(Key={'RecipeName': recipe_name,
            'Ingredients': recipes[0]['Ingredients']})
        return redirect('index')
    if recipes:
        recipe = recipes[0]
        recipe['Ingredients'] = recipe['Ingredients'].split('\n')
        if 'Directions' in recipe:
            recipe['Directions'] = recipe['Directions'].split('\n')
        return render(request, 'view.html', {'recipe': recipe})
    raise Http404("Recipe does not exist.")


def add(request):
    if request.method == 'POST':
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        table = dynamodb.Table('Recipes')
        recipe_name = request.POST['RecipeName']
        recipes = table.query(KeyConditionExpression=Key(
            'RecipeName').eq(recipe_name))['Items']
        if not recipes:
            ingredients = [i for i in request.POST.getlist('Ingredients[]') if i]
            directions = [d for d in request.POST.getlist('Directions[]') if d]
            recipe = {
                'RecipeName': recipe_name,
                'Ingredients': '\n'.join(ingredients)
            }
            if directions:
                recipe['Directions'] = '\n'.join(directions)
            table.put_item(Item=recipe)
            return redirect('view', recipe_name=recipe_name)
    return render(request, 'add.html', {})

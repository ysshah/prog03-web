from django.shortcuts import render, redirect
from django.http import Http404
import boto3

def index(request):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('RecipesDB')
    recipes = table.scan()['Items']
    return render(request, 'index.html', { 'recipes': recipes })


def view(request, recipe_name):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('RecipesDB')
    if request.method == 'POST':
        table.delete_item(Key={'RecipeName': recipe_name})
        return redirect('index')
    query = table.get_item(Key={'RecipeName': recipe_name})
    if 'Item' in query:
        recipe = query['Item']
        recipe['Ingredients'] = recipe['IngredientsList'].split('\n')
        if 'PrepDirections' in recipe:
            recipe['Directions'] = recipe['PrepDirections'].split('\n')
        context = {
            'recipe': recipe,
            'page_title': recipe['RecipeName'] + ' | '
        }
        return render(request, 'view.html', context)
    raise Http404("Recipe does not exist.")


def ingredients(request, recipe_name):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('RecipesDB')
    query = table.get_item(Key={'RecipeName': recipe_name})
    if 'Item' in query:
        recipe = query['Item']
        recipe['Ingredients'] = recipe['IngredientsList'].split('\n')
        context = {
            'recipe': recipe,
            'page_title': recipe['RecipeName'] + ' Ingredients | '
        }
        return render(request, 'ingredients.html', context)
    raise Http404("Recipe does not exist.")


def add(request):
    if request.method == 'POST':
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        table = dynamodb.Table('RecipesDB')
        recipe_name = request.POST['RecipeName']
        query = table.get_item(Key={'RecipeName': recipe_name})
        if 'Item' not in query:
            ingredients = [i for i in request.POST.getlist('Ingredients[]') if i]
            directions = [d for d in request.POST.getlist('Directions[]') if d]
            recipe = {
                'RecipeName': recipe_name,
                'IngredientsList': '\n'.join(ingredients)
            }
            if directions:
                recipe['PrepDirections'] = '\n'.join(directions)
            table.put_item(Item=recipe)
            return redirect('view', recipe_name=recipe_name)
    return render(request, 'add.html', {'page_title': 'Add New Recipe | '})

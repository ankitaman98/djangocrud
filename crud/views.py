from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from django.conf.urls import url
from crud.models import Crud
from crud.serializers import CrudSerializer
from rest_framework.decorators import api_view


@api_view(['GET', 'POST', 'DELETE'])
def crud_list(request):
    if request.method == 'POST':
        tutorial_data = JSONParser().parse(request)
        tutorial_serializer = CrudSerializer(data=tutorial_data)
        if tutorial_serializer.is_valid():
            tutorial_serializer.save()
            return JsonResponse(tutorial_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        tutorials = Crud.objects.all()
        
        title = request.GET.get('title', None)
        if title is not None:
            tutorials = tutorials.filter(title__icontains=title)
        
        tutorials_serializer = CrudSerializer(tutorials, many=True)
        return JsonResponse(tutorials_serializer.data, safe=False)
        
    elif request.method == 'DELETE':
        count = Crud.objects.all().delete()
        return JsonResponse({'message': '{} Tutorials were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)
 
 
@api_view(['GET', 'PUT', 'DELETE'])
def crud_detail(request, pk):
    # find tutorial by pk (id)
    try: 
        tutorial = Crud.objects.get(pk=pk) 
    except Crud.DoesNotExist: 
        return JsonResponse({'message': 'The tutorial does not exist'}, status=status.HTTP_404_NOT_FOUND) 

    if request.method == 'GET': 
        tutorial_serializer = CrudSerializer(tutorial) 
        return JsonResponse(tutorial_serializer.data) 
    
    elif request.method == 'PUT': 
        tutorial_data = JSONParser().parse(request) 
        tutorial_serializer = CrudSerializer(tutorial, data=tutorial_data) 
        if tutorial_serializer.is_valid(): 
            tutorial_serializer.save() 
            return JsonResponse(tutorial_serializer.data) 
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    elif request.method == 'DELETE': 
        tutorial.delete() 
        return JsonResponse({'message': 'Tutorial was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
 
    # GET / PUT / DELETE tutorial
    
        
@api_view(['GET'])
def crud_list_published(request):
    tutorials = Crud.objects.filter(published=True)
        
    if request.method == 'GET': 
        tutorials_serializer = CrudSerializer(tutorials, many=True)
        return JsonResponse(tutorials_serializer.data, safe=False)


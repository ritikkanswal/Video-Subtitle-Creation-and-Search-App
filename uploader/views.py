from django.shortcuts import render
from rest_framework import viewsets, parsers
from .models import Videos
from .serializers import VideosSerializer
import boto3
import subprocess
import tempfile
import os
from botocore.exceptions import ClientError
from django.http import JsonResponse
from SubtitleTimeTracker.celery import app
from django.http import HttpResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from uploader.tasks import save_to_database
# from uploader.tasks import add_numbers
import uuid

AWS_ACCESS_KEY_ID = 'AKIAWJLMVLT3WT2NSIN2'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'videos-ecowiser'
AWS_S3_SIGNATURE_VERSION = 's3v4'
AWS_S3_REGION_NAME = 'eu-north-1'

# s3_client = boto3.client('s3')
dynamodb = boto3.client('dynamodb',
                        aws_access_key_id=AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=AWS_SECRET_ACCESS_KEY ,
                        region_name=AWS_S3_REGION_NAME)

s3 = boto3.client('s3',
                        aws_access_key_id=AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=AWS_SECRET_ACCESS_KEY ,
                        region_name=AWS_S3_REGION_NAME)

def convert_mp4_to_binary(file_path):
    with open(file_path, 'rb') as file:
        binary_data = file.read()
    return binary_data

class VideosViewset(viewsets.ModelViewSet):
 
    queryset = Videos.objects.all()
    serializer_class = VideosSerializer
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
    http_method_names = ['get', 'post', 'patch', 'delete']


def search_in_dynamodb(video_id, search_text):
    # save_to_database.delay("hi")
    # res=add_numbers.delay(1,2)
    # print(res)
    try:
        # Perform the search query
        response = dynamodb.scan(
            TableName='subtitle_data',
            FilterExpression='contains(subtitle_text, :search_text) AND video_id = :video_id',
            ExpressionAttributeValues={
                ':video_id': {'S': video_id},
                ':search_text': {'S': search_text}
            }
        )
        print(response)

        # Extract the results from the response
        items = response.get('Items', [])
        results = []
        for item in items:
            result = {
                'video_id': item.get('video_id', {}).get('S', ''),
                'text': item.get('subtitle_text', {}).get('S', ''),
                'start_time': item.get('start_time', {}).get('S', ''),
                'end_time': item.get('end_time', {}).get('S', ''),
            }
            results.append(result)

        return results

    except ClientError as e:
        print(f"Error searching in DynamoDB: {e}")
        return []


def search_videos(request):
    video_id = request.GET.get('video_id', '')
    search_text = request.GET.get('search_text', '')

    results = search_in_dynamodb(video_id, search_text)

    return JsonResponse({'results': results})

BUCKET_NAME='videos-ecowiser'
from django.views.decorators.csrf import csrf_exempt
from django.core.files.uploadedfile import SimpleUploadedFile

@csrf_exempt
def upload_to_s3(request):
    title = request.POST.get('title','')
    file = request.FILES.get('document')

    bytes_data = file.read()
    import base64
    encoded_data = base64.b64encode(bytes_data).decode('utf-8')


    s3_url=save_to_database.delay(title,encoded_data)

    return HttpResponse(s3_url)

@csrf_exempt
def file_name(request):
    #file_path = file.temporary_file_path()
    file = file=request.FILES.get('document')
    return JsonResponse({'results': "DOne"})



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

    def create(self, request, *args, **kwargs):
        
        print("Trying to Upload subtitile in DyanmoDB!!")

        # Get the uploaded file from the request
        # file = request.data.get('file')
        video_file = request.FILES.get('document')
        file_path = 'media/demo.mp4'

        # Save the file locally
        with open('media'+'demo.mp4', 'wb') as file:
            for chunk in video_file.chunks():
                file.write(chunk)
        file_path='media/demo.mp4'
        # convert_video_to_subtitle(file_path)


        # Call the parent create method to save the file
        return super().create(request, *args, **kwargs)


def convert_video_to_subtitle(path):
    print(path)
    # Run CCExtractor command and capture output
    result = subprocess.run(['ccextractor', '-out=srt', path], capture_output=True, text=True)
    # Check if the CCExtractor command was successful
    if result.returncode == 0:
        # Extracted subtitles are stored in the result.stdout
        subtitles = result.stdout
        path='media/demo.srt'
        parse_srt_file(path,'subtitle_data')
        print(subtitles)
    else:
        # CCExtractor command failed, print the error message
        print(result.stderr)

    print("completed!!")


def parse_srt_file(file_path, table_name):
    # Create a DynamoDB client
    # dynamodb = boto3.client('dynamodb')

    # Open the SRT file for reading
    with open(file_path, 'r') as file:
        subtitles = file.read()

    # Split the subtitles into individual subtitle blocks
    subtitle_blocks = subtitles.strip().split('\n\n')

    # Iterate over each subtitle block
    for block in subtitle_blocks:
        # Split the block into lines
        lines = block.strip().split('\n')
        print(lines)
        # Extract the subtitle index, timestamps, and text
        index = lines[0]
        timestamps = lines[1].split(' --> ')
        start_time = timestamps[0]
        end_time = timestamps[1]
        text = ' '.join(lines[2:])

        # Create an item for the subtitle in the DynamoDB table
        item = {
            'id': {'S': str(index)},  
            'video_id': {'S': str('1')},  
            'start_time': {'S': start_time},
            'end_time': {'S': end_time},
            'subtitle_text': {'S': text}
        }

        print(item)

        # Put the item into the DynamoDB table
        response = dynamodb.put_item(
            TableName=table_name,
            Item=item
        )

        # Print the response (optional)
        print(response)


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
    title=request.POST.get('title','')
    file=request.FILES.get('document')
    bytes_data = file.read()
    import base64
    encoded_data = base64.b64encode(bytes_data).decode('utf-8')


    s3_url=save_to_database.delay(title,encoded_data)

    return HttpResponse(s3_url)





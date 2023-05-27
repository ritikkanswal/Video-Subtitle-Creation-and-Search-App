# from SubtitleTimeTracker.celery import app

from celery import shared_task
import uuid
import boto3
from .serializers import VideosSerializer
import subprocess


AWS_ACCESS_KEY_ID = 'AKIAWJLMVLT3WT2NSIN2'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'videos-ecowiser'
AWS_S3_SIGNATURE_VERSION = 's3v4'
AWS_S3_REGION_NAME = 'eu-north-1'
BUCKET_NAME='videos-ecowiser'
# s3_client = boto3.client('s3')
dynamodb = boto3.client('dynamodb',
                        aws_access_key_id=AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=AWS_SECRET_ACCESS_KEY ,
                        region_name=AWS_S3_REGION_NAME)

s3 = boto3.client('s3',
                        aws_access_key_id=AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=AWS_SECRET_ACCESS_KEY ,
                        region_name=AWS_S3_REGION_NAME)

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

@shared_task
def save_to_database(title,encoded_data):

    serializer = VideosSerializer(data={'title': title, 'link': 'NONE' ,'upload_status':'PENDING','subtitle_upload_status':'PENDING'})
    # serializer.validated_data['upload_status']="COMPLETED"
    if(serializer.is_valid()):
        serializer.save()
    else:
        print("Error")

    
    import base64
    bytes_data = base64.b64decode(encoded_data.encode('utf-8'))
    import io
    f=io.BytesIO(bytes_data)
    file2=f
    file_path='media/demo.mp4'
    # Save the file locally
    with open(file_path, 'wb') as file:
            file.write(bytes_data)
    
    file_path='media/demo.mp4'
    try:
        convert_video_to_subtitle(file_path)
        serializer.validated_data['subtitle_upload_status']="COMPLETED"
    except:
        serializer.validated_data['subtitle_upload_status']="FAILED"
    if(serializer.is_valid()):
        serializer.save()
    else:
        print("Error during saving subtitle")

    try:
        
        unique_key = str(uuid.uuid4())

        file_extension = ".mp4"

        # Construct the S3 key using the unique key and file extension
        s3_key = f"videos/{unique_key}.{file_extension}"

        s3.upload_fileobj(file2, BUCKET_NAME, s3_key)

        # Get the URL of the uploaded file
        s3_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{s3_key}"

        serializer.validated_data['link']=s3_url
        serializer.validated_data['upload_status']="COMPLETED"
        if(serializer.is_valid()):
            serializer.save()
        else:
            print("Error")
    except:
        serializer.validated_data['upload_status']="FAILED"
        if(serializer.is_valid()):
            serializer.save()
        else:
            print("Error")

    return True

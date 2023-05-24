# from SubtitleTimeTracker.celery import app

from celery import shared_task
import uuid
import boto3
from .serializers import VideosSerializer
AWS_ACCESS_KEY_ID = 'AKIAWJLMVLT3WT2NSIN2'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'videos-ecowiser'
AWS_S3_SIGNATURE_VERSION = 's3v4'
AWS_S3_REGION_NAME = 'eu-north-1'
BUCKET_NAME='videos-ecowiser'

s3 = boto3.client('s3',
                        aws_access_key_id=AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=AWS_SECRET_ACCESS_KEY ,
                        region_name=AWS_S3_REGION_NAME)
                      
@shared_task
def save_to_database(title,encoded_data):

    serializer = VideosSerializer(data={'title': title, 'link': 'NONE' ,'upload_status':'PENDING'})
    # serializer.validated_data['upload_status']="COMPLETED"
    if(serializer.is_valid()):
        serializer.save()
    else:
        print("Error")
    try:
        import base64
        bytes_data = base64.b64decode(encoded_data.encode('utf-8'))

        import io
        f=io.BytesIO(bytes_data)
        file2=f
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

    return s3_url

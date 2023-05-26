from rest_framework.routers import SimpleRouter
from .views import VideosViewset
from .views import search_videos
from .views import upload_to_s3
from .views import file_name
from django.urls import path, include  

router = SimpleRouter()
router.register('accounts', VideosViewset)
urlpatterns = [
    # Add your custom URLs here
    path('api/search/', search_videos, name='search-api'),  # new
    path('upload/', VideosViewset.as_view({'post': 'upload'}), name='upload'),
    path('api/upload/', upload_to_s3, name='upload_to_s3'),  # new
    path('api/file_name/', file_name, name='file_name'),  # new
    # Include the router URLs
] + router.urls
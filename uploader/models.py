from django.db import models

 
class Videos(models.Model):
    title = models.CharField(max_length=100)
    link = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    upload_status = models.CharField(max_length=100,default="PENDING")
    
    class Meta:
        verbose_name_plural = 'Videos'
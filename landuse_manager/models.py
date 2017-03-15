from django.db import models

# Create your models here.


class Document(models.Model):
	doc_name = models.CharField(max_length=50, blank=True)
	document = models.FileField(upload_to='', blank=True)

class FileManagerDocument(models.Model):
	doc_name = models.CharField(max_length=50, blank=True)
	date_modified = models.CharField(max_length=50, blank=True)
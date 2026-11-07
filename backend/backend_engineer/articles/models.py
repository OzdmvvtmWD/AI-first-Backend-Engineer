from django.db import models

# Create your models here.
class Article():

    article_name = models.CharField(max_length=510, unique=True)
    article_text = models.TextField()
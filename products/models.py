from django.db import models
from django.db.models.fields import CharField, DateTimeField, TextField
from django.db.models.fields.files import ImageField

class Product(models.Model):
    name = CharField(max_length=100)
    image = ImageField()
    category = CharField(max_length=100)
    description = TextField()
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField()

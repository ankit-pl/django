from django.db import models
from django.db.models.fields import IntegerField

class Poll(models.Model):
    user_id = models.IntegerField()
    product_id = models.IntegerField()
    vote_up = models.BooleanField()
    vote_down = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField()

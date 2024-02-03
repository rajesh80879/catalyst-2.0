from django.db import models

# Create your models here.

import uuid

class Record(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, null=True, blank=True)
    domain = models.CharField(max_length=255, null=True, blank=True)
    year_founded = models.PositiveIntegerField(null=True, blank=True)
    industry = models.CharField(max_length=255, null=True, blank=True)
    size_range = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    linkedin_url = models.URLField(null=True, blank=True)
    current_employees = models.PositiveIntegerField(null=True, blank=True)
    total_employees = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.id)


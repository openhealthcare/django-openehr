from django.db import models
from django_openehr.models.demographics import Demographics


class Identifier(models.Model):
    # implements RM class 'ID' Identifier as a class
    demographics = models.ForeignKey(
        Demographics,
        on_delete=models.CASCADE
    )

    issuer = models.CharField(max_length=255, blank=True)
    assigner = models.CharField(max_length=255, blank=True)
    identifier = models.CharField(max_length=255)  # mandatory
    identifier_type = models.CharField(max_length=255, blank=True)

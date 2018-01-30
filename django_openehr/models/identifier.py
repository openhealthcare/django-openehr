from django.db import models


class Identifier(models.Model):
    # implements RM class 'ID' Identifier as a class

    issuer = models.CharField(max_length=255, blank=True, null=True)
    assigner = models.CharField(max_length=255, blank=True, null=True)
    identifier = models.CharField(max_length=255)  # mandatory
    identifier_type = models.CharField(max_length=255, blank=True, null=True)

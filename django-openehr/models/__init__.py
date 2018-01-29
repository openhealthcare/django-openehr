from django.db import models

from django_openehr.models.address_details import AddressDetails
from django_openehr.models.telecom_details import TelecomDetails
from django_openehr.models.demographics import Demographics
from django_openehr.models.symptom_sign import SymptomSign
from django_openehr.models.therapeutic_direction import TherapeuticDirection, TherapeuticDirectionDosage

__all__ = ['AddressDetails', 'TelecomDetails', 'Demographics', 'SymptomSign', 'TherapeuticDirection', 'TherapeuticDirectionDosage']


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

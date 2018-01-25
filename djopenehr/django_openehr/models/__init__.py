from django.db import models

# //noticed a bit of an issue with this archetype:
# 'Relationship to Subject' kind of implies that this is not Demographics about
# the EHR's Subject (the patient) but someone else.

# It is suggested that we might use the FHIR CareConnect demographic model instead:
# https://www.hl7.org/fhir/STU3/patient.html

from django_openehr.models.address_details import AddressDetails
from django_openehr.models.telecom_details import TelecomDetails
from django_openehr.models.demographics import Demographics
from django_openehr.models.symptom_sign import SymptomSign

__all__ = ['AddressDetails', 'TelecomDetails', 'Demographics', 'SymptomSign']


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

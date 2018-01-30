from django.db import models
from django_openehr.models.identifier import Identifier
from django_openehr.models.person_name import PersonName
from django_openehr.models.telecom_details import TelecomDetails


class DemographicProfessional(models.Model):
    # openEHR-EHR-CLUSTER.individual_professional_uk.v1

    class Meta():
        verbose_name_plural = "Professional Demographics"

    # Name
    # Slot (Cluster)
    # Optional
    # Personal name details of the individual.
    # openEHR-EHR-CLUSTER.person_name.v1
    # implemented in class models.person_name()
    person_name = models.ManyToManyField(
        PersonName,
    )

    # Telecoms
    # Slot (Cluster)
    # Optional, repeating
    # implemented in class models.telecom_details()
    telecom_details = models.ManyToManyField(
        TelecomDetails,
    )

    # Organisation
    # Slot ( Cluster)
    # Optional, repeating
    # Organisation details to which the individual is attached.
    # openEHR-EHR-CLUSTER.organisation.v1 and specialisations
    # TODO

    # Professional group
    # Text
    # Optional
    professional_group = models.CharField(
        blank=True, null=True,
        help_text="The professional group or speciality of the professional",
        max_length=255,
    )

    # Grade
    # Text
    # Optional
    professional_grade = models.CharField(
        blank=True, null=True,
        help_text="The employment grade or position of the carer",
        max_length=255
    )

    # Team
    # Text
    # Optional
    professional_team = models.CharField(
        blank=True, null=True,
        help_text="Team to which the individual belongs",
        max_length=255
    )

    # Professional Identifier
    # Identifier
    # Optional, repeating
    professional_identifier = models.ManyToManyField(
        Identifier,
    )

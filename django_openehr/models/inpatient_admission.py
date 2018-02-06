from django.db import models
from django_openehr.models.demographic_professional import DemographicProfessional


class InpatientAdmission(models.Model):
    # implements openEHR-EHR-ADMIN_ENTRY.inpatient_admission_uk.v1

    # Date of admission
    # Date/Time
    # Optional
    date_of_admission = models.DateTimeField(
        null=True, blank=True,
        auto_now=False,
        auto_now_add=False,
        help_text="Date patient admitted to hospital"
    )

    # Admission method
    # Choice
    # Optional
    ADMISSION_METHOD_CHOICES = (
        ("ELECTIVE", "Elective [The admission was planned.]"),
        ("EMERGENCY", "Emergency [The admission was made as an emergency.]"),
        ("TRANSFER", "Transfer [The patient was transferred from another inpatient unit.]"),
        ("MATERNITY", "Maternity [The admission was maternity-related.]"),
    )
    admission_method = models.CharField(
        blank=True, null=True,
        max_length=255,
        help_text="How the patient was admitted to hospital")

    # Referrer details
    # Slot ( Cluster)
    # Optional
    # Details of person making the request for admission.
    # Include:
    # All not explicitly excluded archetypes
    referrer_details = models.ManyToManyField(
        DemographicProfessional,
        blank=True,
    )

    # Source of admission
    # Text
    # Optional
    # Comment: eg, usual place of residence, temporary place of residence, penal establishment.
    source_of_admission = models.CharField(
        blank=True, null=True,
        max_length=255,
        help_text="The locaton of the patient immediately prior to admission"
    )

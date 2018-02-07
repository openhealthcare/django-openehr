from django.db import models


class ClinicalSynopsis(models.Model):
    # implements openEHR-EHR-EVALUATION.clinical_synopsis.v1

    class Meta:
        verbose_name_plural = "Clinical Synopses"

    # Synopsis
    # Text
    # Mandatory
    synopsis = models.TextField(
        help_text="The summary, assessment, conclusions or evaluation of the clinical findings",
    )

from django.db import models


class ReasonForEncounter(models.Model):
    # implements openEHR-EHR-EVALUATION.reason_for_encounter.v1

    class Meta():
        verbose_name_plural = "Reasons for Encounter"

    # Contact type
    # Text
    # Optional, repeating
    # Comment: Coding of the 'Contact type' with a terminology is desirable, where possible. Examples include: pre-employment medical, routine antenatal visit, women's health check, pre-operative # assessment, or annual medical check-up.
    contact_type = models.CharField(
        blank=True, null=True,
        max_length=255,
        help_text="Identification of the type, or administrative category, of healthcare sought or required by the subject of care."
    )

    # Presenting problem
    # Text
    # Optional, repeating
    # Comment: Coding of the 'Presenting problem' with a terminology is desirable, where possible. Clinical or social reasons for seeking healthcare can include health issues, symptoms or physical signs. Examples: health issues - desire to quit smoking, domestic violence; symptoms - abdominal pain, shortness of breath; physical signs - an altered conscious state. 'Chief complaint' may be # used as a valid synonym for 'Presenting problem' in templates.
    presenting_problem = models.CharField(
        blank=True, null=True,
        max_length=255,
        help_text="Identification of the clinical or social problem motivating the subject of care to seeking healthcare."
    )
    # TODO Consider if this should actually contain an instance of Problem/Diagnosis object rather than a free text/terminology field

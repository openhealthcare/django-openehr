from django.db import models


class TelecomDetails(models.Model):
    # implements openEHR-EHR-CLUSTER.telecom_uk.v1

    class Meta():
        verbose_name_plural = "Telecoms Details"

    # suspected typo in archetype openEHR-EHR-CLUSTER.telecom_uk.v1
    # first field 'unstuctured_telcoms' should be 'UnstRuctured telEcoms'
    # text
    # optional
    unstructured_telecoms = models.TextField(
        null=True,
        blank=True,
        help_text="An unstructured description of telecoms."
    )

    # Country code
    # text
    # optional
    country_code = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        help_text="Telephone country code. ENV13606-4:2000 7.11.18."
    )

    # Area code
    # text
    # optional
    area_code = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        help_text="Telephone area code."
    )

    # Number
    # text
    # optional
    number = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        help_text="Telephone number."
    )

    # Extension
    # text
    # optional
    extension = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        help_text="Telephone extension number. ENV13606-4:2000 7.11.18."
        )

    # Method
    # Text
    # optional
    method = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="The communications mode, eg Fax, Skype, Landline, Mobile etc"
        )

    # Use context
    # Text
    # Optional
    use_context = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="the context of use of this telecom contact eg Home, Work, Business")

    def __str__(self):
        if self.number:
            return self.number
        elif self.unstructured_telecoms:
            return self.unstructured_telecoms
        else:
            return 'telephone number not held'

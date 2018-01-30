from django.db import models


class AddressDetails(models.Model):
    # implements openEHR-EHR-CLUSTER.address.v1

    class Meta():
        verbose_name_plural = "addresses"

    ADDRESS_TYPE_CHOICES = (
        ("RESIDENTIAL", "Residential"),
        ("CORRESPONDENCE", "Correspondence"),
        ("BUSINESS", "Business"),
        ("TEMPORARY", "Temporary")
    )

    # coded text
    # mandatory
    address_type = models.CharField(
        max_length=255,
        choices=ADDRESS_TYPE_CHOICES,
        help_text="The type of address."
    )

    # text
    # optional
    unstructured_address = models.TextField(
        null=True,
        blank=True,
        help_text="A postal address expressed in an unstructured format."
    )

    # text
    # optional
    property_number = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        help_text="The number of the property."
    )

    # text
    # optional
    # Address Line in the archetype has cardinality 0..4 => 4 address lines
    address_line1 = models.CharField(max_length=255, null=True, blank=True)
    address_line2 = models.CharField(max_length=255, null=True, blank=True)
    address_line3 = models.CharField(max_length=255, null=True, blank=True)
    address_line4 = models.CharField(max_length=255, null=True, blank=True)

    # text
    # optional
    post_code = models.CharField(
        null=True,
        blank=True,
        max_length=20,
        help_text="Post code.")

    # Address Valid Period:cluster:interval_of_date/time:optional
    # The period during which the associated address is applicable to the
    # person / organisation. ENV 13606 - 4:2000 7.11.11. This describes the
    # actual period.
    # see issue https://github.com/openhealthcare/django-openehr/issues/5
    validity_period_from = models.DateTimeField(
        null=True,
        blank=True,
        help_text="The start of the period for which this address is valid."
    )

    validity_period_to = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Date from which the address is no longer valid."
    )

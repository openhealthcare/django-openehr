from django.db import models
from django.core.exceptions import ValidationError
from django_openehr.models.address_details import AddressDetails
from django_openehr.models.identifier import Identifier
from django_openehr.models.person_name import PersonName
from django_openehr.models.telecom_details import TelecomDetails


class DemographicPersonal(models.Model):
    # from openEHR-EHR-CLUSTER.individual_personal_uk.v1
    # where slots exist they have been filled with the appropriate archetype

    class Meta():
        verbose_name_plural = "Personal Demographics"

    # PERSON NAME
    # optional
    # presumably repeated, because you can't have an 'AKA' as the only name in
    # a system (although it doesn't say 'repeated' in the UK CKM)
    # slot:accepts cluster openEHR-EHR-CLUSTER.person_name.v1
    # implemented in class models.person_name.PersonName()

    person_name = models.ManyToManyField(
        PersonName,
    )

    # ADDRESS_DETAILS
    # optional, repeated
    # slot:accepts cluster (openEHR-EHR-CLUSTER.address_uk.v0)
    # implemented in class models.address_details.AddressDetails()
    address_details = models.ManyToManyField(
        AddressDetails,
    )

    # TELECOM_DETAILS
    # optional, repeated
    # slot:acceptscluster (openEHR-EHR-CLUSTER.telecom_uk.v1)
    # implemented in class models.telecom_details.TelecomDetails()
    telecom_details = models.ManyToManyField(
        TelecomDetails,
    )

    # relationship_to_subject
    relationship_to_subject = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="The relationship of this individual to the subject e.g. family member, informal carer."
    )

    # IDENTIFIER is a reference model data type
    # implemented in class models.identifier.Identifier()
    identifier = models.ManyToManyField(
        Identifier,
    )

    # date_of_birth
    # optional
    date_of_birth = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Individual's date of birth."
    )

    # gender
    # optional
    GENDER_CHOICES = (
        ('FEMALE', 'Female'),
        ('MALE', 'Male'),
        ('UNSPECIFIED', 'Unspecified')
    )
    gender = models.CharField(
        max_length=255,
        choices=GENDER_CHOICES,
        null=True,
        blank=True,
        help_text="The administrative phenotypical gender of the individual."
    )

    def clean(self):
        """
        Validation that requires access to multiple fields goes here.
        """
        structured_name_fields = [
            'title'
            'given_name',
            'middle_name',
            'family_name',
            'suffix'
        ]
        present = 0
        for f in structured_name_fields:
            if getattr(self, f) is not None:
                present += 1
        if present == 1:
            msg = "A structured name requires at least two of {0}".format(
                ", ".join(structured_name_fields)
            )
            raise ValidationError(msg)

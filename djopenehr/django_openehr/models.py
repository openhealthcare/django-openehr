from django.db import models

# //noticed a bit of an issue with this archetype:
# 'Relationship to Subject' kind of implies that this is not Demographics about
# the EHR's Subject (the patient) but someone else.

# It is suggested that we might use the FHIR CareConnect demographic model instead:
# https://www.hl7.org/fhir/STU3/patient.html


class Demographics(models.Model):
    # from openEHR-EHR-CLUSTER.individual_personal_uk.v1
    # where slots exist they have been filled with the appropriate archetype

    # ## NAME ## #
    # optional
    # presumably repeated, because you can't have an 'AKA' as the only name in
    #    a system (although it doesn't say 'repeated' in the UK CKM)
    # slot:acceptscluster
    # openEHR-EHR-CLUSTER.person_name.v1 has been 'flattened' into this model

    # ## name_type:coded_text:optional
    # suggested values from CKM are
    NAME_TYPE_CHOICES = (
        ('REGISTERED',   'Registered name [The name by which the subject is officially registered.]'),
        ('PREVIOUS',     'Previous name [Name previously used by this person.]'),
        ('BIRTH',        'Birth name [Name given to this person at birth.]'),
        ('AKA',          'AKA [Person also known as.]'),
        ('ALIAS',        'Alias [Other name used by this person.]'),
        ('MAIDEN',       'Maiden Name [Name used by this persion before marriage.]'),
        ('PROFESSIONAL', 'Professional name [The name used by the subject for business or professional purposes.]'),
        ('REPORTING',    'Reporting name [The subject’s name as it is to be used for reporting, when used with a specific identifier.]'),
    )
    name_type = models.CharField(
        max_length=256,
        choices=NAME_TYPE_CHOICES,
        blank=True,
        help_text="The type of name described"
    )

    # ## preferred_name
    # boolean
    # optional
    preferred_name = models.BooleanField(
        blank=True,
        help_text="Indicates that this is the name by which a person chooses to be identified."
    )

    # unstructured_name:text:optional
    unstructured_name = models.CharField(
        max_length=256,
        blank=True,
        help_text="Name in free text unstructured format."
    )

    # ## Structured name ## #
    # cluster:optional:Minimum of 2 items
    # Name in structured format.

    # title:text:optional
    # no canonical list of titles was suggested in the archetype
    # FHIR, NHS data dictionary also do not have a canonical list
    TITLE_CHOICES = (
        ('DR', 'Dr.'),
        ('MRS', 'Mrs.'),
        ('MR', 'Mr.'),
        ('MISS', 'Miss'),
        ('MS', 'Ms.'),
        ('PROF', 'Prof.'),
        ('SIR', 'Sir'),
        ('REV', 'Rev'),
    )

    title = models.CharField(
        max_length=20,
        choices=TITLE_CHOICES,
        blank=True,
        help_text="The prefix or title used by the subject, e.g. Mr, Mrs, Ms, Dr, Lord"
    )

    # text:mandatory
    given_name = models.CharField(
        max_length=256,
        help_text="Given / personal / first name."
    )

    # middle_name:text:optional:repeating
    # 'Coded Text' in the UK CKM but I don't think they really mean that
    middle_name = models.CharField(
        max_length=256,
        blank=True,
        help_text="Middle name or names."
    )

    # family_name:text:mandatory
    family_name = models.CharField(
        max_length=256,
        help_text="Family name or Surname.")

    # suffix:text:optional
    suffix = models.CharField(
        max_length=20,
        blank=True,
        help_text="Additional term used following a person name, e.g. 'Snr'")

    # validity_period:interval_of_date/time:optional
    validity_period_from = models.DateTimeField(
        help_text="The date from which this name was valid."
    )
    validity_period_to = models.DateTimeField(
        help_text="The date until which this name was valid."
    )

    # ADDRESS_DETAILS
    # optional, repeated
    # slot:acceptscluster (openEHR-EHR-CLUSTER.address_uk.v0)
    # implemented in class AddressDetails()

    # TELECOM_DETAILS
    # optional, repeated
    # slot:acceptscluster (openEHR-EHR-CLUSTER.telecom_uk.v1)
    # implemented in class TelecomDetails()

    # relationship_to_subject
    relationship_to_subject = models.CharField(
        max_length=256,
        blank=True,
        help_text="The relationship of this individual to the subject e.g. family member, informal carer."
    )

    # IDENTIFIER is a reference model data type
    # implemented in class Identifier()

    # date_of_birth
    # optional
    date_of_birth = models.DateTimeField(
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
        choices=GENDER_CHOICES,
        blank=True,
        help_text="The administrative phenotypical gender of the individual."
    )

    class AddressDetails(models.model):
        # implements openEHR-EHR-CLUSTER.address.v1

        demographics = models.ForeignKey(
            Demographics
        )

        ADDRESS_TYPE_CHOICES = (
            ("RESIDENTIAL", "Residential"),
            ("CORRESPONDENCE", "Correspondence"),
            ("BUSINESS", "Business"),
            ("TEMPORARY", "Temporary")
        )

        # coded text
        # mandatory
        address_type = CharField(
            max_length=256,
            choices=ADDRESS_TYPE_CHOICES,
            help_text="The type of address."
        )

        # text
        # optional
        unstructured_address = models.TextField(
            blank=True,
            help_text="A postal address expressed in an unstructured format."
        )

        # text
        # optional
        property_number = models.CharField(
            max_length=20,
            blank=True,
            help_text="The number of the property."
        )

        # text
        # optional
        # Address Line in the archetype has cardinality 0..4 => 4 address lines
        address_line1 = models.CharField(max_length=256, blank=True)
        address_line2 = models.CharField(max_length=256, blank=True)
        address_line3 = models.CharField(max_length=256, blank=True)
        address_line4 = models.CharField(max_length=256, blank=True)

        # text
        # optional
        post_code = models.CharField(
            max_length=20,
            help_text="Post code.")

        # Address Valid Period:cluster:interval_of_date/time:optional
        # The period during which the associated address is applicable to the person /
        # organisation. ENV 13606 - 4:2000 7.11.11. This describes the actual period.
        #
        # AddressValid Period in openEHR-EHR-CLUSTER.address.v1 is implemented as a CLUSTER with
        # Valid from and Valid to Date/Time values, whereas a very similar attribute of
        # openEHR-EHR-CLUSTER.person_name.v1, Validity period, is implemented as an Interval of
        # Date/Time.
        validity_period_from = models.DateTimeField(
            help_text="The start of the period for which this address is valid."
        )
        validity_period_to   = models.DateTimeField(
            help_text="Date from which the address is no longer valid."
        )


    class TelecomDetails(models.Model):
        # implements openEHR-EHR-CLUSTER.telecom_uk.v1

        demographics = models.ForeignKey(Demographics)

        # suspected typo in archetype openEHR-EHR-CLUSTER.telecom_uk.v1
        # first field 'unstuctured_telcoms' should be 'UnstRuctured telEcoms'
        # text
        # optional
        unstructured_telecoms = models.TextField(
            help_text="An unstructured description of telecoms."
        )

        # Country code
        # text
        # optional
        country_code = models.CharField(
            max_length=20,
            blank=True,
            help_text="Telephone country code. ENV13606-4:2000 7.11.18."
        )

        # Area code
        # text
        # optional
        area_code = models.CharField(
            max_length=20,
            blank=True,
            help_text="Telephone area code."
        )

        # Number
        # text
        # optional
        number = models.CharField(
            max_length=20,
            blank=True,
            help_text="Telephone number."
        )

        # Extension
        # text
        # optional
        extension = models.CharField(
            max_length=20,
            blank=True,
            help_text="Telephone extension number. ENV13606-4:2000 7.11.18."
            )

        # Method
        # Text
        # optional
        method = models.CharField(
            max_length=256,
            blank=True,
            help_text="The communications mode, eg Fax, Skype, Landline, Mobile etc"
            )

        # Use context
        # Text
        # Optional
        use_context = models.CharField(
            max_length=256,
            blank=True,
            help_text="the context of use of this telecom contact eg Home, Work, Business")


    class Identifier(models.model):
        # implements RM class 'ID' Identifier as a class
        demographics = models.ForeignKey(Demographics)

        issuer = models.CharField(max_length=256, blank=True)
        assigner = models.CharField(max_length=256, blank=True)
        identifier = models.CharField(max_length=256)  # mandatory
        identifier_type = models.CharField(max_length=256, blank=True)

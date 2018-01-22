from django.db import models

# //noticed a bit of an issue with this archetype:
# 'Relationship to Subject kind of implies that this is not Demographics about
# the EHR's Subject (the patient) but someone else


class Demographics(models.Model):
    # from openEHR-EHR-CLUSTER.individual_personal_uk.v1
    # where slots exist they have been filled with the appropriate archetype

    ### NAME ###
    # optional
    # presumably repeated, because you can't have an 'AKA' as the only name in
    #    a system (although it doesn't say 'repeated' in the UK CKM)
    # slot:acceptscluster
    # openEHR-EHR-CLUSTER.person_name.v1 has been 'flattened' into this model

    ### name_type:coded_text:optional
    # Type of Name Described
    # suggested values from CKM are
    NAME_TYPE_CHOICES=(
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
    )

    ### preferred_name:boolean:optional
    # allowed values: {true} //well, duh... or,  maybe, false?
    # Indicates that this is the name by which a person chooses to be identified.
    preferred_name = models.BooleanField()

    # unstructured_name:text:optional
    # Name in free text unstructured format.
    unstructured_name = models.CharField(max_length=256)

    ### Structured name ###
    # cluster:optional:Minimum of 2 items
    # Name in structured format.

    # title:text:optional
    # The prefix or title used by the subject.
    # e.g. 'Mr', 'Mrs', 'Ms', 'Dr', 'Lord' //no canonical list suggested in the archetype
    # //FHIR, NHS data dictionary also do not have a canonical list
    TITLE_CHOICES=(
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
    choices=TITLE_CHOICES
    )

    # text:mandatory
    # Given / personal / first name.
    given_name = models.CharField(max_length=256)

    # middle_name:text:optional:repeating
    # 'Coded Text' in the UK CKM but I don't think they really mean that
    # Middle name or names.
    middle_name = models.CharField(max_length=256)

    # family_name:text:mandatory
    # Family name or Surname.
    family_name = models.CharField(max_length=256)

    # suffix:text:optional
    # Additional term used following a person name, e.g. 'Snr'
    suffix = models.CharField(max_length=20)

    # validity_period:interval_of_date/time:optional
    # The date interval at which this name was valid.
    validity_period_from = models.DateTimeField
    validity_period_to   = models.DateTimeField

    # address_details
    # optional, repeated
    # slot:acceptscluster (openEHR-EHR-CLUSTER.address_uk.v0)
    # implemented in class AddressDetails()


    # telecom_details
    # optional, repeated
    # slot:acceptscluster (openEHR-EHR-CLUSTER.telecom_uk.v1)
    # implemented in class TelecomDetails()


    # relationship_to_subject
    relationship_to_subject = models.CharField(max_length=256)

    # identifier is a reference model data type
    # implemented in class Identifier()


    # date_of_birth
    # optional
    date_of_birth = models.DateTimeField()

    # gender
    # optional
    GENDER_CHOICES = (
        ('FEMALE', 'Female'),
        ('MALE', 'Male'),
        ('UNSPECIFIED', 'Unspecified')
    )
    gender = models.CharField(
        choices=GENDER_CHOICES
    )

    class AddressDetails(models.model):
        demographics = models.ForeignKey(
            Demographics
        )

        ADDRESS_TYPE_CHOICES=(
            ("RESIDENTIAL", "Residential"),
            ("CORRESPONDENCE", "Correspondence"),
            ("BUSINESS", "Business"),
            ("TEMPORARY", "Temporary")
        )

        address_type = CharField (
            max_length=256,
            choices=ADDRESS_TYPE_CHOICES
        )

        unstructured_address = models.TextField()

        property_number = models.CharField(max_length=20)

        # Address Line in the archetype has cardinality 0..4 => 4 address lines
        address_line1 = models.CharField(max_length=256)
        address_line2 = models.CharField(max_length=256)
        address_line3 = models.CharField(max_length=256)
        address_line4 = models.CharField(max_length=256)

        post_code = models.CharField(max_length=20)

        # Address Valid Period:cluster:interval_of_date/time:optional
        # The date interval at which this address was valid.
        #
        # AddressValid Period in openEHR-EHR-CLUSTER.address.v1 is implemented as a CLUSTER with
        # Valid from and Valid to Date/Time values, whereas a very similar attribute of
        # openEHR-EHR-CLUSTER.person_name.v1, Validity period, is implemented as an Interval of
        # Date/Time.

        validity_period_from = models.DateTimeField
        validity_period_to   = models.DateTimeField


    class TelecomDetails(models.Model):
        # implements archetype openEHR-EHR-CLUSTER.telecom_uk.v1

        demographics = models.ForeignKey(Demographics)

        # suspected typo in archetype openEHR-EHR-CLUSTER.telecom_uk.v1
        # first field 'unstructured_telcoms' should be 'telecoms'
        unstructured_telecoms = models.TextField()

        # Country code:text:optional
        country_code = models.CharField(max_length=20)

        # Area code:text:optional
        area_code = models.CharField(max_length=20)

        # Number:text:optional
        number = models.CharField(max_length=20)

        # Extension:text:optional
        extension = models.CharField(max_length=20)

        # The communications mode, eg Fax, Skype, Landline, Mobile etc
        method = models.CharField(max_length=256)

        # the context of use of this telecom contact eg Home, Work, Business
        use_context = models.CharField(max_length=256)


    class Identifier(models.model):
        # implements RM class 'ID' Identifier as a class
        demographics = models.ForeignKey(Demographics)

        issuer = models.CharField(max_length=256)
        assigner = models.CharField(max_length=256)
        identifier = models.CharField(max_length=256)
        identifier_type = models.CharField(max_length=256)

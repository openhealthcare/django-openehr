from django.core.validators import MinValueValidator
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
        max_length=200,
        choices=NAME_TYPE_CHOICES,
    )

    ### preferred_name:boolean:optional
    # allowed values: {true} //well, duh... or,  maybe, false?
    # Indicates that this is the name by which a person chooses to be identified.
    preferred_name = models.BooleanField()

    # unstructured_name:text:optional
    # Name in free text unstructured format.
    unstructured_name = models.CharField(max_length=200)

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
    given_name = models.CharField(max_length=200)

    # middle_name:text:optional:repeating
    # 'Coded Text' in the UK CKM but I don't think they really mean that
    # Middle name or names.
    middle_name = models.CharField(max_length=200)

    # family_name:text:mandatory
    # Family name or Surname.
    family_name = models.CharField(max_length=200)

    # suffix:text:optional
    # Additional term used following a person name, e.g. 'Snr'
    suffix = models.CharField(max_length=20)

    # validity_period:interval_of_date/time:optional
    # The date interval at which this name was valid.
    validity_period_from = models.DateTimeField
    validity_period_to   = models.DateTimeField

    # address_details
    # optional, repeated
    # slot:acceptscluster:flattened
    # => openEHR-EHR-CLUSTER.address_uk.v0


    # telecom_details
    # optional, repeated
    # slot:acceptscluster:flattened


    # relationship_to_subject
    relationship_to_subject = models.CharField(max_length=200)

    # identifier

    # date_of_birth
    # optional

    # gender
    # optional


class TherapeuticDirection(models.Model):
    # Direction sequence
    # Count
    # Optional
    # min: >=1
    direction_sequence = models.IntegerField(
        blank=True, null=True,
        help_text="The intended position of this direction within the overall sequence of directions."
        validators=[MinValueValidator(1)]
    )
    # Dosage Implemented in TherapeuticDirectionDosage
    # The combination of a medication dose and administration timing for a single day.
    # Include:
    # openEHR-EHR-CLUSTER.dosage.v1 and specialisations

    # Direction duration
    # Choice
    # Optional
    # The length of time for which this direction should be applied.

    DIRECTION_CHOICES = (
        # The direction should be continued indefinitely.
        ('INDEFINITE', 'Indefinite'),
        # The direction should be continued indefinitely with a strong recommendation
        # that it never be discontinued.
        ('INDEFINITENTBDC', 'Indefinite - not to be discontinued')
    )
    # Choice of one of the following three fields:

    direction_duration = models.CharField(
        choices=DIRECTION_CHOICES, blank=True, null=True, max_length=255
    )
    # Duration >=0 seconds
    direction_duration_seconds = models.IntegerField(
        validators=[MinValueValidator(0)]
        blank=True, null=True
    )
    # Text
    direction_duration_text = models.CharField(
        blank=True, null=True, max_length=255
    )

    # Maximum number of administrations
    # Count
    # Optional
    # min: >=1
    maximum_administrations = models.IntegerField(
        blank=True, null=True,
        validators=[MinValueValidator(1)]
        help_text="The maximum number of administrations to be given for this direction."
    )

    # Direction repetition
    # Slot ( Cluster)
    # Optional

    # Structured details about pattern of repetition for each set of daily directions.
    # Include:
    # nopenEHR-EHR-CLUSTER.timing_repetition.v0 and specialisations
    # Included




    # Additional details
    # Slot ( Cluster)
    # Optional, repeating

    # Further details about an ordered item direction.

    # Include:
    # openEHR-EHR-CLUSTER.conditional_medication_rules.v0 and specialisations

    def clean(self):
        """
        Validation that requires access to multiple fields goes here.
        """
        direction_duration_fields = [
            'direction_duration',
            'direction_duration_seconds',
            'direction_duration_text'
        ]
        present = 0
        for f in direction_duration_fields:
            if getattr(self, f) is not None:
                present += 1
        if present > 1:
            msg = "A direction duration may only be one of {0}".format(
                ", ".join(structured_name_fields)
            )
            raise ValidationError(msg)


class TherapeuticDirectionDosage(models.Model):
    therapeutic_direction = models.ForeignKey(TherapeuticDirection)
    # openEHR-EHR-CLUSTER.dosage.v1 and specialisations

    # Dosage sequence
    #  Count
    # Optional
    # The intended position of this dosage within the overall sequence of dosages.
    # Comment: For example: '1', '2', '3'. Where multiple dosages are expressed, the 'Pattern sequence' makes the order in which they should be executed explicit. For example: (1) 1 tab in the morning, (2) 2 tab at 2pm, (3) 1 tab at night.
    # min: >=1

    # Dose amount
    #  Choice
    # Optional
    # The value of the amount of medication administered at one time, as a real number, or range of real numbers, and associated with the Dose unit.
    # Comment: For example: 1, 1.5, 0.125 or 1-2, 12.5-20.5
    # Choice of:
    #  Quantity
    # Property: Qualified real
    # Units:
    # >=0.0 1
    #  Interval of Quantity

# Lower: Property: Qualified real
    # Units:
    # >=0.0 1

# Upper: Property: Qualified real
    # Units:
    # >=0.0 1

# Dose unit
    #  Text
    # Optional
    # The unit which is associated with the Dose amount.
    # Comment: For example: 'tablet','mg'. Coding of the dose unit with a terminology is preferred, where possible.


# Dose formula
    #  Choice
    # Optional
    # The formula used to calculate the dose amount or administration rate where this is dependent on some other factor, such as body weight or surface area.
    # Comment: For example: '10mg/kg/day'. The result of this formula would normally be held in Dose amount/unit or Administration rate/duration. Where clinical measurements such as body weight is used in the dose calculation, a LINK attribute should used to specify which particular measurement has been used.
    # Choice of:
    #  Text
    #  Quantity
    # Dose description
    #  Text
    # Optional
    # Text description of the dose.
    # Comment: For example: "Apply ointment to affected area until it glistens". This element is intended to allow implementers to use the structures for increasing/tapering dosages without necessarily specifying the doses in a structured way.


# Timing
    # Slot ( Cluster)
    # Optional, repeating
    # Structured details about the timing pattern for a single day.
    # Comment: For example: 'in the morning', 'at 0600, 1400, 2100'.
    # Include:
    # openEHR-EHR-CLUSTER.timing_daily.v0 and specialisations

# Included

# Administration rate
    #  Choice
    # Optional
    # The rate at which the medication, such as an infusion, is to be administered.
    # Comment: For example: '200 ml/h'. Use the text data type to record non- or semi-quantifiable instructions.
    # Choice of:
    #  Quantity
    # Property: Flow rate, volume
    # Units:
    # >=0.0 l/h
    # >=0.0 ml/min
    # >=0.0 ml/s
    # >=0.0 ml/h
    #  Text
    # Administration duration
    #  Duration
    # Optional
    # The period of time over which a single dose of the medication or vaccine should be administered.
    # Comment: For example: 'Administer over 10 minutes'.
    # Allowed values: days, hours, minutes, seconds
    # >=0 hours
    # Alternate dose amount
    #  Choice
    # Optional
    # An alternate representation of the value of the amount of medication administered at one time, as a real number, or range of real numbers, and associated with the Dose unit.
    # Comment: For example, can be used to represent a unit-dose based value such as 'tabs', when the Dose amount is expressed as an SI unit such as 'mg', or where it is required to express the total amount of an infusion as well as the dose amount of the active ingredient.
    # Choice of:
    #  Quantity
    # Property: Qualified real
    # Units:
    # >=0.0 1
    #  Interval of Quantity

# Lower: Property: Qualified real
    # Units:
    # >=0.0 1

# Upper: Property: Qualified real
    # Units:
    # >=0.0 1

# Alternate dose unit
    #  Text
    # Optional
    # The unit which is associated with the Alternate dose amount.

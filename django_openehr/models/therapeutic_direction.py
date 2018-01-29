from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models


class TherapeuticDirection(models.Model):
    # Direction sequence
    # Count
    # Optional
    # min: >=1
    direction_sequence = models.IntegerField(
        blank=True, null=True,
        help_text="The intended position of this direction within the overall sequence of directions.",
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
        # The direction should be continued indefinitely with a strong
        # recommendation that it never be discontinued.
        ('INDEFINITENTBDC', 'Indefinite - not to be discontinued')
    )
    # Choice of one of the following three fields:

    direction_duration = models.CharField(
        choices=DIRECTION_CHOICES, blank=True, null=True, max_length=255
    )
    # Duration >=0 seconds
    direction_duration_seconds = models.IntegerField(
        validators=[MinValueValidator(0)],
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
        validators=[MinValueValidator(1)],
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
    therapeutic_direction = models.ForeignKey(
        TherapeuticDirection,
        on_delete=models.CASCADE)
    # openEHR-EHR-CLUSTER.dosage.v1 and specialisations

    # Dosage sequence
    # Count
    # Optional
    # Comment: For example: '1', '2', '3'. Where multiple dosages are
    # expressed, the 'Pattern sequence' makes the order in which they should be
    # executed explicit. For example: (1) 1 tab in the morning, (2) 2 tab at
    # 2pm, (3) 1 tab at night.
    # min: >=1
    dosage_sequence = models.IntegerField(
        blank=True, null=True,
        help_text="The intended position of this dosage within the overall sequence of dosages.",
        validators=[MinValueValidator(1)]
    )

    # Dose amount
    # Choice
    # Optional
    # The value of the amount of medication administered at one time, as a real
    # number, or range of real numbers, and associated with the Dose unit.
    # Comment: For example: 1, 1.5, 0.125 or 1-2, 12.5-20.5
    # Choice of: Quantity or Interval of Quantity
    # Property: Qualified real
    # >=0.0 1
    dose_amount_exact = models.DecimalField(
        blank=True, null=True,
        max_digits=10,
        decimal_places=3,
        help_text="The value of the amount of medication administered at one time, as a real number, or range of real numbers, and associated with the Dose unit.",
        validators=[MinValueValidator(0.01)]
    )

# Lower: Property: Qualified real
    # >=0.0 1
    dose_amount_range_lower = models.DecimalField(
        blank=True, null=True,
        max_digits=10,
        decimal_places=3,
        validators=[MinValueValidator(0.01)],
        help_text="Lower limit of the dose range",)

# Upper: Property: Qualified real
    # >=0.0 1
    dose_amount_range_upper = models.DecimalField(
        blank=True, null=True,
        max_digits=10,
        decimal_places=3,
        validators=[MinValueValidator(0.01)],
        help_text="Upper limit of the dose range")

# Dose unit
    # Text
    # Optional
    # Comment: For example: 'tablet','mg'. Coding of the dose unit with a terminology is preferred, where possible.
    dose_unit = models.CharField(
        blank=True, null=True,
        help_text="The unit which is associated with the Dose amount.",
        max_length=255
    )

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

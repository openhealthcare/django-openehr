from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class BodySite(models.Model):
    pass

class SymptomSign(models.Model):
    # Symptom/Sign name
    # Text
    # Mandatory
    # [SNOMED-CT::19019007]
    # Comment: Symptom name should be coded with a terminology, where possible.
    symptom_sign_name = models.CharField(
        max_length=255,
        help_text="The name of the reported symptom or sign."
    )

    # Nil significant
    # Boolean
    # Optional
    nil_significant = models.NullBooleanField(
        null=True,
        blank=True,
        help_text="The identified symptom or sign was reported as not being present to any significant degree."
    )

    # Description
    # Text
    # Optional
    # [SNOMED-CT::162408000 | General symptom description (finding)]
    description = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Narrative description about the reported symptom or sign."
    )

    # Body site
    # Text
    # Optional, repeating
    # recommended use is to use clinical terminology
    body_site = models.ManyToManyField(
        BodySite,
        null=True,
        blank=True,
        help_text="Simple body site where the symptom or sign was reported."
    )

    # Structured body site has been OMITTED in favour of using terminology
    # in the Body Site field above.
    # Slot ( Cluster)
    # Optional, repeating
    # Structured body site where the symptom or sign was reported.
    # Comment: If the anatomical location is included in the Symptom name via
    # precoordinated codes, use of this SLOT becomes redundant. If the
    # anatomical location is recorded using the 'Body site' data element,
    # then use of CLUSTER archetypes in this SLOT is not allowed
    # - record only the simple 'Body site' OR 'Structured body site'
    # but not both.
    # Include:
    # openEHR-EHR-CLUSTER.anatomical_location.v1 and specialisations Or
    # openEHR-EHR-CLUSTER.anatomical_location_clock.v0 Or
    # openEHR-EHR-CLUSTER.anatomical_location_relative.v1

    # Episodicity
    # Coded Text
    # Optional
    EPISODICITY_CHOICES = (
        ("NEW", "New"),
        # A new episode of the symptom or sign - either the first ever
        # occurrence or a reoccurrence # where the previous episode had
        # completely resolved.]
        ("ONGOING", "Ongoing"),
        # This symptom or sign is ongoing, a single, continuous episode.]
        ("INDETERMINATE", "Indeterminate")
        # Indeterminate [It is not possible to determine if this occurrence of
        # the symptom or sign is new or # ongoing.]
    )
    episodicity = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        choices=EPISODICITY_CHOICES,
        help_text="Category of this episode for the identified symptom or sign."
    )

    # First ever?
    # Boolean
    # Optional
    first_ever = models.NullBooleanField(
        blank=True,
        help_text="Is this the first ever occurrence of this symptom or sign?"
    )

    # Episode onset
    # Date/Time
    # Optional
    episode_onset = models.DateTimeField(
        null=True,
        blank=True,
        help_text="The onset for this episode of the symptom or sign.",
    )

    # Onset type
    # Text
    # Optional
    onset_type = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Description of the onset of the symptom or sign eg gradual or sudden."
    )

    # Duration
    # Optional
    # [SNOMED-CT::162442009 | Time symptom lasts (observable entity)]
    # Comment: If 'Date/time of onset' and 'Date/time of resolution' are used
    # in systems, this data element may be calculated, or alternatively, be
    # considered redundant in this scenario.
    duration = models.DateTimeField(
        null=True,
        blank=True,
        help_text="The duration of this episode of the symptom or sign since onset"
    )


    # Severity category
    # Choice
    # Optional
    SEVERITY_CATEGORIES_CHOICES = (
        ("MILD", "Mild [The intensity of the symptom or sign does not cause interference with normal activity.] [SNOMED-CT::162468002] (Symptom mild (finding)"),
        ("MODERATE", "Moderate: Moderate [The intensity of the symptom or sign causes interference with normal activity.] [SNOMED-CT::162469005] (Symptom moderate (finding)"),
        ("SEVERE", "Severe: Severe [The intensity of the symptom or sign prevents normal activity.] [SNOMED-CT::162470006] (Symptom severe (finding)")
    )
    severity_category = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        choices=SEVERITY_CATEGORIES_CHOICES,
        help_text="Category representing the overall severity of the symptom or sign."
    )

    # Severity rating
    # Quantity
    # Optional, repeating
    severity_rating = models.DecimalField(
        null=True,
        blank=False,
        max_digits=1,
        decimal_places=1,
        validators=[MaxValueValidator(10.0), MinValueValidator(0.0)],
        max_length=1,
    )
    # Comment: Symptom severity can be rated by the individual by recording a
    # score from 0 (ie symptom not present) to 10.0 (ie symptom is as severe
    # as the individual can imagine). This score can be represented in the user
    # interface as a visual analogue scale. The data element has occurrences
    # set to 0..* to allow for variations such as 'maximal severity' or
    # 'average severity' to be included in a template.

    # Progression
    # Coded Text
    # Optional, repeating
    # Comment: Occurrences of this data element are set to 0..* to allow
    # multiple types of progression to be separated out in a template if
    # desired - for example, severity or frequency.
    PROGRESSION_CHOICES = (
        ("WORSENING","Worsening [The severity of the symptom or sign has worsened overall during this episode.]"),
        ("UNCHANGED","Unchanged [The severity of the symptom or sign has not changed overall during this episode.]"),
        ("IMPROVING","Improving [The severity of the symptom or sign has improved overall during this episode.]"),
        ("RESOLVED","Resolved [The severity of the symptom or sign has resolved.]")
    )
    progression = models.CharField(
        max_length=255,
        choices=PROGRESSION_CHOICES,
        null=True,
        blank=True,
        help_text="Description progression of the symptom or sign at the time of reporting."
    )

    # Pattern
    # Text
    # Optional
    # Comment: For example: pain could be described as constant or intermittent.
    pattern = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        help_text="Narrative description about the pattern of the symptom or sign during this episode."
    )

    # MODIFYING FACTOR
    # Cluster
    # Optional, repeating
    # Detail about how a specific factor effects the identified symptom or sign
    # during this episode.

    # Factor
    # Text
    # Optional
    # Comment: Examples of modifying factor: lying on multiple pillows,
    # eating or administration of a specific medication.
    modifying_factor_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Name of the modifying factor.",
    )

    # Effect
    # Coded Text
    # Optional
    EFFECT_CHOICES = (
        ("Relieves", "Relieves [The factor decreases the severity or impact of the symptom or sign, but does not fully # resolve it.]"),
        ("NOEFFECT", "No effect [The factor has no impact on the symptom or sign.]"),
        ("WORSENS", "Worsens [The factor increases the severity or impact of the symptom or sign.]")
    )
    modifying_factor_effect = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        choices=EFFECT_CHOICES,
        help_text="Perceived effect of the modifying factor on the symptom or sign."
    )

    # Description
    # Text
    # Optional
    modifying_factor_effect_description = models.TextField(
        null=True,
        blank=True,
        help_text="Narrative description of the effect of the modifying factor on the symptom or sign."
    )

    # (Precipitating/resolving factor)
    # Cluster
    # Optional, repeating
    # Details about specified factors that are associated with the
    # precipitation or resolution of the # symptom or sign.
    # Comment: For example: onset of headache occurred one week prior to
    # menstruation; or onset of # headache occurred one hour after fall off
    # bicycle.
    # Runtime name constraint: (not implemented in the Django version)
    # Precipitating factor [Identification of factors or events that trigger the
    # onset or commencement of # the symptom or sign.]
    # Resolving factor [Identification of factors or events that trigger
    # resolution or cessation of the # symptom or sign.]

    # Factor
    # Text (MB: coded text perhaps more useful here?)
    # Optional
    # Comment: For example: onset of another symptom; onset of menstruation; or fall off bicycle.
    precipitating_resolving_factor_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Name of the health event, symptom, reported sign or other factor.",

    )

    # Factor detail
    # Slot ( Cluster)
    # Optional, repeating
    # Structured detail about the factor associated with the identified symptom
    # or sign.
    # Include:
    # openEHR-EHR-CLUSTER.health_event.v1 and specialisations Or
    # openEHR-EHR-CLUSTER.symptom_sign.v0 (MB: oh, clever - recursion, awesome)

    # Time interval
    # Duration
    # Optional
    precipitating_resolving_factor_interval = models.DateTimeField(
        null=True,
        blank=True,
        help_text="The interval of time between the occurrence or onset of the factor and onset/resolution of the # symptom or sign."
    )

    # Description
    # Text
    # Optional
    precipitating_resolving_factor_description = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Narrative description about the effect of the factor on the identified symptom or sign."
    )

    # Impact
    # Text
    # Optional, repeating
    # Comment: Assessment of impact could consider the severity, duration and
    # frequency of the symptom as well as the type of impact including, but not
    # limited to, functional, social and emotional impact. Occurrences of this
    # data element are set to 0..* to allow multiple types of impact to be
    # separated out in a template if desired. Examples for functional impact
    # from hearing loss may include: 'Difficulty Hearing in Quiet Environment';
    # 'Difficulty Hearing the TV or Radio'; # 'Difficulty Hearing Group
    # Conversation'; and 'Difficulty Hearing on Phone'.
    impact = models.TextField(
        null=True,
        blank=True,
        help_text="Description of the impact of this symptom or sign.",
    )

    # Episode description
    # Text
    # Optional
    #  Comment: For example: a text description of the immediate onset of the
    #  symptom, activities that worsened or relieved the symptom, whether it is
    #  improving or worsening and how it resolved over weeks.
    episode_description = models.TextField(
        null=True,
        blank=True,
        help_text="",
    )

    # Specific details
    # Slot ( Cluster)
    # Optional, repeating
    # Specific data elements that are additionally required to record as unique
    # attributes of the # identified symptom or sign.
    # Comment: For example: CTCAE grading.
    # Include:
    # All not explicitly excluded archetypes
    # MB: I'm really not sure what this adds to recording of a symptom

    # Resolution date/time
    # Date/Time
    # Optional
    #  Comment: If 'Date/time of onset' and 'Duration' are used in systems, this
    #  data element may be calculated, or alternatively, considered redundant.
    #  While partial dates are permitted, the exact date and time of
    #  resolution can be recorded, if appropriate.
    resolution_date_time = models.DateTimeField(
        null=True,
        blank=True,
        help_text="The timing of the cessation of this episode of the symptom or sign.",
    )

    # Description of previous episodes
    # Text
    # Optional
    # Comment: For example: frequency/periodicity - per hour, day, week, month, year; and regularity. May # include a comparison to this episode.
    previous_episode_description = models.TextField(
        null=True,
        blank=True,
        help_text="Narrative description of any or all previous episodes."
    )

    # Number of previous episodes
    # Count
    # Optional
    # The number of times this symptom or sign has previously occurred.
    # min: >=0      # MB: yes, obviously it's not a negative number


    # Previous episodes
    # Slot ( Cluster)
    # Optional, repeating
    # Structured details of the symptom or sign during a previous episode.
    #  Comment: In linked clinical systems, it is possible that previous
    #  episodes are already recorded within the EHR. Systems can allow the
    #  clinician to LINK to relevant previous episodes. However in a system or
    #  message without LINKs to existing data or with a new patient, additional
    #  instances of the symptom archetype could be included here to represent
    #  previous episodes. It is recommended that new instances of the Symptom
    #  archetype inserted in this SLOT represent one or many previous # episodes
    #  to this Symptom instance only.
    # openEHR-EHR-CLUSTER.symptom_sign.v0 and specialisations
    # MB: handled as a ManyToManyField recursive to self
    associated_symptom_sign = models.ManyToManyField(
        "self",
        null=True,
        blank=True,
        help_text="Structured details about any associated symptoms or signs that are concurrent."
    )

    # Associated symptom/sign
    # Slot ( Cluster)
    # Optional, repeating
    #  Comment: In linked clinical systems, it is possible that associated
    #  symptoms or signs are already recorded within the EHR. Systems can allow
    #  the clinician to LINK to relevant associated symptoms/signs. However in a
    #  system or message without LINKs to existing data or with a new patient,
    #  additional instances of the symptom archetype could be included here to
    #  represent # associated symptoms/signs.
    #  openEHR-EHR-CLUSTER.symptom_sign.v0 and specialisations
    #  MB: handled as a ManyToManyField recursive to self
    associated_symptom_sign = models.ManyToManyField(
        "self",
        null=True,
        blank=True,
        help_text="Structured details about any associated symptoms or signs that are concurrent."
    )

    # Comment
    # Text
    # Optional
    symptom_comment = models.TextField(
        null=True,
        blank=True,
        help_text="Additional narrative about the symptom or sign not captured in other fields."
    )

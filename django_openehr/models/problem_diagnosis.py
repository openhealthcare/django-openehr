from django.db import models


class ProblemDiagnosis(models.Model):
    # implements openEHR-EHR-EVALUATION.problem_diagnosis.v1

    class Meta:
        verbose_name_plural = "Problems / Diagnoses"

    # Problem/Diagnosis name
    # Text
    # Mandatory
    # Comment: Coding of the name of the problem or diagnosis with a terminology is preferred, where # possible.
    problem_diagnosis_name = models.CharField(
        null=True,
        max_length=255,
        help_text="Identification of the problem or diagnosis, by name"
    )

    # Clinical description
    # Text
    # Optional
    # Comment: Use to provide background and context, including evolution, episodes or exacerbations, # progress and any other relevant details, about the problem or diagnosis.
    clinical_description = models.TextField(
        blank=True, null=True,
        help_text="Narrative description about the problem or diagnosis"
    )

    # Body site
    # Text
    # Optional, repeating
    # Comment: Coding of the name of the anatomical location with a terminology is preferred, where possible. Use this data element to record precoordinated anatomical locations. If the requirements for recording the anatomical location are determined at run-time by the application or require more complex modelling such as relative locations then use the CLUSTER.anatomical_location or CLUSTER.relative_location within the 'Structured anatomical location' SLOT in this archetype. Occurrences for this data element are unbounded to allow for clinical scenarios such as describing a rash in multiple locations but where all of the other attributes are identical. If the anatomical location is included in the # Problem/diagnosis name via precoordinated codes, this data element becomes redundant.
    body_site_name = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        help_text="The identifier of the body site, using a recognised clinical terminology where possible"
    )

    # Structured body site has been OMITTED in favour of using terminology
    # in the Body Site field above.


    # Date/time of onset
    # Date/Time
    # Optional
    # Comment: Data captured/imported as "Age at onset" should be converted to a date using the # subject's date of birth.
    onset_date_time = models.DateTimeField(
        blank=True, null=True,
        help_text="Estimated or actual date/time that signs or symptoms of the problem/diagnosis were first observed",
    )

    # Date/time clinically recognised
    # Date/Time
    # Optional
    # Comment: Partial dates are acceptable. If the subject of care is under the age of one year, then the complete date or a minimum of the month and year is necessary to enable accurate age calculations - for example, if used to drive decision support. Data captured/imported as "Age at time of clinical recognition" should be converted to a date using the subject's date of # birth.
    recognition_date_time = models.DateTimeField(
        blank=True, null=True,
        help_text="Estimated or actual date/time the diagnosis or problem was recognised by a healthcare professional.",
    )

    # Severity
    # Choice
    # Optional
    # Comment: If severity is included in the Problem/diagnosis name via precoordinated codes,
    # this data element becomes redundant. Note: more specific grading of severity
    # can be recorded using # the Specific details SLOT.
    # Choice of:
    # Coded Text
    SEVERITY_CHOICES = (
        ("Mild", "Mild [The problem or diagnosis does not interfere with normal activity or may cause damage to health if left untreated.]"),
        ("Moderate", "Moderate [The problem or diagnosis causes interference with normal activity or will damage health if left untreated.]"),
        ("Severe", "Severe [The problem or diagnosis prevents normal activity or will seriously damage health if left untreated.]"),
    )
    severity = models.CharField(
        blank=True, null=True,
        choices=SEVERITY_CHOICES,
        max_length=255,
        help_text="An assessment of the overall severity of the problem or diagnosis",
    )
    # TODO ForeignKeyOrFreeText would work here, also SNOMED-CT terms instead


    # Specific details
    # Slot (Cluster)
    # Optional, repeating
    # Comment: May include structured detail about the grading or staging of the diagnosis;
    # diagnostic criteria, classification criteria or formal severity assessments such
    # as Common Terminology Criteria for Adverse Events.
    # Include:
    # All not explicitly excluded archetypes
    # NOTE (@pacharanero): I have no idea what possible use this could have in an EHR. Omitted.

    # Course description
    # Text
    # Optional
    course_description = models.TextField(
        blank=True, null=True,
        help_text="Narrative description about the course of the problem or diagnosis since onset",
    )

    # Date/time of resolution
    # Date/Time
    # Optional
    # Comment: Partial dates are acceptable. If the subject of care is under the age of one year
    # then the complete date or a minimum of the month and year is necessary to enable accurate
    # age calculations - for example, if used to drive decision support. Data captured/imported
    # as "Age at time of resolution" should be converted to a date using the subject's date of birth.
    resolution_date_time = models.DateTimeField(
        blank=True, null=True,
        help_text="Estimated or actual date/time of resolution or remission for this problem or diagnosis, as determined by a healthcare professional",
    )

    # Status
    # Slot ( Cluster)
    # Optional, repeating
    # Structured details for location-, domain-, episode- or workflow-specific aspects of the # diagnostic process.
    # Comment: Use status or context qualifiers with care, as they are variably used in
    # practice and interoperability cannot be assured unless usage is clearly defined with
    # the community of use. For example: active status - active, inactive, resolved, in
    # remission; evolution status - initial, interim/working, final; temporal status -
    # current, past; episodicity status - first, new, ongoing; admission status - admission, discharge; or priority status - primary, # secondary.
    # Include:
    # openEHR-EHR-CLUSTER.problem_status.v0 and specialisations
    # NOTE (@pacharanero): I'm pretty sure there's nothing in the openEHR-EHR-CLUSTER.problem_status.v0
    # archetype that cannot be represented better in SNOMED-CT

    # Diagnostic certainty
    # Choice
    # Optional
    # Choice of Coded Text or Text
    # The level of confidence in the identification of the diagnosis.
    DIAGNOSTIC_CERTAINTY_CHOICES = (
        ("Suspected", "Suspected [The diagnosis has been identified with a low level of certainty.]"),
        ("Probable", "Probable [The diagnosis has been identified with a high level of certainty.]"),
        ("Confirmed", "Confirmed [The diagnosis has been confirmed against recognised criteria.]"),
    )
    diagnostic_certainty = models.CharField(
        blank=True, null=True,
        choices = DIAGNOSTIC_CERTAINTY_CHOICES,
        max_length=255,
        help_text="The level of confidence in the identification of the diagnosis"
    )

    # Last updated
    # Date/Time
    # Optional
    last_updated = models.DateTimeField(
        blank=True, null=True,
        help_text="The date this problem or diagnosis was last updated",
    )

    # Comment
    # Text
    # Optional
    comment = models.CharField(
        blank=True, null=True,
        max_length=255,
        help_text="Any random comment you can't fit into one of the other 572 fields in this archetype"
    )

    def __str__(self):
        if self.problem_diagnosis_name:
            return self.problem_diagnosis_name
        else:
            return "anonymous problem / diagnosis"

from django.db import models


class AdverseReaction(models.Model):
    # implements openEHR-EHR-EVALUATION.adverse_reaction_uk.v1

    # Causative agent
    # Choice
    # Mandatory
    # TODO this is a field that would benefit from FreeTextOrForeignKey implementation
    causative_agent = models.CharField(
        null=True,  # required to avoid having to specify a default value in Django
        max_length=255,
        help_text="Details of the agent or medicinal substance believed to be the cause of the adverse reaction or allergy")
    # Comment: For GP2GP V2 use, it is currently anticipated that there will be 4 permissible ways to express a Causative agent: Drug Group (SNOMED-CT), dm+d VMP/AMP (dm+d), Ingredient (SNOMED-CT), TradeFamily/TradeFamilyGroup (SNOMED-CT). It is MANDATORY that one and only one of these must always be selected. Optionally, in addition a SNOMED AllergyCode may be sent as a mapping, but can never be sent on its own. For legacy use other codes are permissible such as FDB Agent codes, EMIS Drug codes and READ codes but these should be carried as simple free text and the coded information carried in mappings/translation attributes. This kind of coding is not regarded as being safe to trigger decision support outwith the native GP system. The exact subset definitions    # have not yet been agreed and may change prior to full implementation.
    # Choice of Coded Text or Text
    # Constraint: Causative Agent: A causative agent term from one of the approved terminology subsets - dm+d Ingredient/VTM/AMP/VMP/SNOMED-CT Allergy codes/Trade family/Trade Family Group codes.

    # Reaction details
    # Cluster
    # Optional
    # Details of a single reaction thought to be due to the causative agent.

    # Reaction
    # Coded Text
    # Optional
    # MUST USE CHILD CODE FROM [SNOMED-CT::282100009 | Adverse reaction to substance (disorder)]
    # Constraint: Clinical Finding SNOMED-CT term in the Clinical Finding hierarchy.
    # Constraint binding: [SNOMED-CT] subset=ClinicalFinding
    reaction_snomed_code = models.CharField(
        blank=True, null=True,
        max_length=255,
        help_text="An optional pre-coordinated unqualified SNOMED-CT code for the nature of the reaction produced by the drug allergy")

    # Date recorded
    # Date/Time
    # Optional
    # Comment: From Welsh IHR / openHR model.
    date_recorded = models.DateTimeField(
        null=True, blank=True,
        auto_now=False,
        auto_now_add=False,
        help_text="The date that the reaction was clinically recorded/asserted. This will often equate to the date of  # onset of the reaction but this may not be wholly clear from source data"
    )

    # Severity
    # Coded Text
    # Optional
    # [SNOMED-CT::272141005 | Severities (qualifier value)]
    # Comment: This item has a Translation Set = Read Code (V2 or CTV3) and Snomed Code to ensure
    # forwards and backwards compatibility.
    # Mild [The reaction was mild.]
    # [SNOMED-CT::255604002] (Mild (qualifier value))
    # Moderate [The reaction was moderate.]
    # [SNOMED-CT::6736007] (Moderate (severity modifier) (qualifier value))
    # Severe [The reaction was severe.]
    # [SNOMED-CT::24484000] (Severe (severity modifier) (qualifier value))
    # Life-threatening [The reaction was life-threatening.]
    # [SNOMED-CT::442452003] (Life threatening severity (qualifier value))
    # Fatal [The reaction was fatal.]
    reaction_severity = models.CharField(
        blank=True, null=True,
        max_length=255,
        help_text="The severity of the reaction")

    # Certainty
    # Coded Text
    # Optional
    # [SNOMED-CT::255544004 | Certainties (qualifier value)]
    # Unlikely [The reaction is thought unlikely to have been caused by the agent.]
    # [SNOMED-CT::1491118016]
    # Likely [The reaction is thought likely to have been caused by the agent.]
    # [SNOMED-CT::5961011]
    # Certain [The agent is thought to be certain to have caused the reaction but this has not been confirmed by challenge testing.]
    # [SNOMED-CT::255545003] (Definite (qualifier value))
    # Confirmed by challenge testing [The reaction to the agent has been confirmed by challenge testing or other concrete evidence.]
    # [SNOMED-CT::410605003] (Confirmed present (qualifier value))
    # Comment: This item has a Translation Set between Read Codes (V2 or CTV3) and Snomed Codes to ensure forwards and backwards compatibility.
    reaction_certainty = models.CharField(
        blank=True, null=True,
        max_length=255,
        help_text="The certainty with which the reaction is deemed to be be due to allergy to the agent"
    )

    # Comment
    # Text
    # Optional
    # Comment: From Welsh IHR model
    reaction_comment = models.CharField(
        blank=True, null=True,
        max_length=255,
        help_text="Any additional comment or clarification about the adverse reaction"
    )

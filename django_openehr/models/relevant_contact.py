from django.db import models
from django_openehr.models.person_name import PersonName
from django_openehr.models.telecom_details import TelecomDetails


class RelevantContact(models.Model):
    # implements openEHR-EHR-ADMIN_ENTRY.relevant_contact_rcp.v0

    # Personal details
    # Slot (Cluster)
    # Optional, repeating
    # Personal details of the informal carer.
    # Include:
    # All not explicitly excluded archetypes

    # NOTE the archetype for relevant contact does not specify a type of archetype that can go in this slot, however the intended use (IDCR ToC Template) specifies Person Name and Telecom Details.
    person_name = models.ManyToManyField(
        PersonName,
    )

    telecom_details = models.ManyToManyField(
        TelecomDetails,
    )

    # Relationship category
    # Coded Text
    # Optional
    RELATIONSHIP_CATEGORY_CHOICES = (
        ("INFORMAL_CARER", "Informal carer [An individual identified by the person as offering care and support, excluding paid carers or carers from voluntary agencies.]"),
        ("MAIN_INFORMAL", "Main informal carer [The contact is identified by the subject as being a primary informal source of care and support.]"),
        ("FORMAL_CARE_WORKER", "Formal care worker [A health and social care professional or staff member, including a carer from voluntary sector.]"),
        ("KEY_FORMAL_CARE_WORKER", "Key formal care worker [The formal carer is the subject's key worker.]")
    )
    relationship_category = models.CharField(
        blank=True, null=True,
        max_length=255,
        choices=RELATIONSHIP_CATEGORY_CHOICES,
        help_text="The broad category of care relationship which the contact holds with the subject."
    )

    # Relationship
    # Text
    # Optional
    relationship = models.CharField(
        blank=True, null=True,
        max_length=255,
        help_text="For an informal carer, the personal relationship with the client/carer e.g spouse or friend . For a formal carer, the professional role or responsibility of the carer with respect to the person which should help identify them as being an appropriate contact for an aspect of care, usually a professional role or care pathway name."
    )

    # Is next of kin?
    # Boolean
    # Optional
    is_next_of_kin = models.NullBooleanField(
        null=True,
        blank=True,
        help_text="True if this informal carer is the person's next-of-kin",
    )

    # Note
    # Text
    # Optional
    relationship_note = models.CharField(
        blank=True, null=True,
        max_length=255,
        help_text='Any additional comment or note about the healthcare professional or carer or their role'
    )

    # Date updated
    # Date/Time
    # Optional
    date_updated = models.DateTimeField(
        null=True, blank=True,
        auto_now=False,
        auto_now_add=False,
        help_text="The date at which the list of key contacts was created or updated.",
    )

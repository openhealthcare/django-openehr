from django.db import models


class BodySite(models.Model):
    body_site_name = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        help_text="The identifier of the body site, using a recognised clinical terminology where possible"
    )

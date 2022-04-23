from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField


class TermsAndConditions(models.Model):
    buyer_terms_and_conditions = RichTextUploadingField(
        help_text= 'Elaborate the Terms and Conditions Buyers are subjects to. Please be clear in your explanation.'
    )
    event_organizer_terms_and_conditions = RichTextUploadingField(
        help_text='Terms and Conditions for Event Owners. This must be clear and straight forward to understand.'
    )
    privacy_policy = RichTextUploadingField(
        help_text= 'Describe how you shall maintain security on the information that users are proving to All1Zed '
                   'Events Platform. '
    )
    terms_of_use = RichTextUploadingField(
        help_text='By using All1Zed Events Platform, all stakeholders agree to your specific terms. Describe them here.'
    )


    def __str__(self):
        return 'Terms And Conditions'

    class Meta:
        verbose_name_plural = 'Terms And Conditions'
        verbose_name = 'Terms And Conditions'


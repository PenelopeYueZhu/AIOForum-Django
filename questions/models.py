from django.db import models
from django.utils.text import slugify
from django.urls import reverse

import uuid
import itertools

# Create your models here.

# Abstract parent model for questions. Contains information that all private
# and public questions should have
# Does not actually function as a model that holds information
class Question(models.Model):
    """ Some constants. """
    # Choices for status of the question.
    PUBLIC = 'p'
    ANSWERED = 'a'
    NEW = 'n'

    # Question status
    STATUS = (
        (NEW, 'New'),
        (ANSWERED, 'Answered'),
        (PUBLIC, 'Public'),
    )

    # max_length.
    SLUG_MAX_LENGTH = 200
    SUBJECT_MAX_LENGTH = 140
    CONTENT_MAX_LENGTH = 1000
    STATUS_MAX_LENGTH = 1

    # A unique slug for each question: as URL identifier
    slug = models.SlugField(unique = True,
        default='',
        max_length=SLUG_MAX_LENGTH)

    # Subject of the question
    subject = models.CharField(max_length = SUBJECT_MAX_LENGTH,
        help_text='Summarize your question.')

    # Content of the question
    content = models.TextField(max_length = CONTENT_MAX_LENGTH,
        help_text='State your question here')

    # The date and time of the post. Edited automatically
    post_date = models.DateTimeField(auto_now_add = True)

    # Reply edited later by peer.
    reply =  models.TextField(max_length=CONTENT_MAX_LENGTH,
        help_text='State your reply here',
        null=True, blank=True,)

    # categories of the question. Only editable by the admin
    category = models.ManyToManyField('Category',
        help_text='Select categories applicable for this question',
        blank=True)

    # If the op wants to get an email notification, optional
    # Will be removed once the reply has been sent
    op_email = models.EmailField(blank = True)

    status = models.CharField(
        max_length = STATUS_MAX_LENGTH,
        choices = STATUS,
        blank = True,
        default = 'n',
        help_text = 'Question status.'
    )

    class Meta:
        # Set to display the newest first
        ordering = ['-post_date']

    # Generate a unique slug by adding a unique number after the title.
    # Reference:
    """
    https://djangosnippets.org/snippets/10643/
    """
    def _generate_slug(self):
        # First get the original slugified result.
        origin_slug = slugify(self.subject)
        unique_slug = origin_slug
        # Loop through all slugs to check uniqueness.
        numb = 1
        while Question.objects.filter(slug=unique_slug).exists():
            unique_slug = '%s-%d' % (origin_slug, numb)
            numb += 1

        self.slug = unique_slug

    def save(self, *args, **kwargs):
        # If new record is being created, generate the slug.
        if self._state.adding:
            self._generate_slug()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        kwargs = {'slug': self.slug, 'pk': self.pk}
        return reverse('question-detail', kwargs=kwargs)

    # Set this instance's status to answered.
    def set_to_answered(self):
        self.status = 'a'

    # Set this instance's status to public.
    def set_to_public(self):
        self.status = 'p'

# Category model to hold information about a category
class Category(models.Model):
    """Constants."""
    # max_length.
    NAME_MAX_LENGTH = 100
    """Model representing the category of a question"""
    name = models.CharField(max_length = NAME_MAX_LENGTH,
        help_text = 'Enter the name of the category')

    def __str__(self):
        """String for representing this category object"""
        return self.name

# Reply model to hold information about a reply
class Reply(models.Model):
    """Constants"""
    # max_length.
    CONTENT_MAX_LENGTH = 1000
    """Model representing a reply to a question"""

    # Content of the reply
    content = models.TextField(max_length = CONTENT_MAX_LENGTH,
        help_text = 'State your reply here')

    # The date and time of the reply. Edited automatically
    post_date = models.DateTimeField(auto_now = True)

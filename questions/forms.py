from django import forms
from django.forms.models import modelformset_factory

from questions.models import Category, Question, Reply

# For students to submit a question.
class SubmitQuestionForm(forms.Form):
    subject = forms.CharField(
        help_text='Summarize your question under 100 words.',
        max_length=100)

    content = forms.CharField(
        help_text='Explain it further there',
        widget=forms.Textarea,
        max_length=1000)

    email = forms.EmailField(
        help_text='Optional. Receive notification.',
        required=False)

class BaseCategoryFormSet(forms.BaseModelFormSet):
    """ Validate formset: make sure there is no duplicate names
        for categories."""

    def clean(self):
        """Check if the category has already existed."""
        if any(self.errors): # If any individual data has error, it's error.
            return

        # Get an array of category names already existed.
        existed_categories = Category.objects.all();
        existed_names = []
        for category in existed_categories:
            existed_names.append(category.name)

        # Array to store duplicated category names.
        duplicate_names = []
        # Check if there are repeating category names.
        for form in self.forms:
            # Get each category name from form.
            name = form.cleaned_data.get('name')
            # If name already existed, raise error to let user know.
            if name in existed_names and not name in duplicate_names:
                duplicate_names.append(name)
            else:
                existed_names.append(name)

        # If the duplicated list is not empty, raise an error.
        if duplicate_names:
            raise forms.ValidationError(
                ('Duplicated category: %(name)s'),
               code='duplicate',
               params={'name': ' '.join(duplicate_names)},
            )

# Allow user to add as many categories as they want, one at a time.
CategoryFormSet = modelformset_factory(Category, formset=BaseCategoryFormSet,
    fields=('name',), extra=0, can_delete=True)

from django.test import TestCase
from questions.forms import SubmitQuestionForm

# Class containing methods to test SubmitQuestionForm
class SubmitQuestionFormTest(TestCase):
    # The subject field has a label 'subject'.
    def test_subject_form_char_field_label(self):
        form = SubmitQuestionForm()
        self.assertTrue(form.fields['subject'].label == None
            or form.fields['subject'].label == 'subject')

    # The subject field has the correct helper text.
    def test_subject_form_char_field_help_text(self):
        form = SubmitQuestionForm()
        self.assertEqual(form.fields['subject'].help_text,
            'Summarize your question under 100 words.')

    # The content field has a label 'subject'.
    def test_content_form_char_field_label(self):
        form = SubmitQuestionForm()
        self.assertTrue(form.fields['content'].label == None
            or form.fields['content'].label == 'content')

    # The subject field has the correct helper text.
    def test_content_form_char_field_help_text(self):
        form = SubmitQuestionForm()
        self.assertEqual(form.fields['content'].help_text,
            'Explain it further there')

    # The email field has a label 'subject'.
    def test_email_form_char_field_label(self):
        form = SubmitQuestionForm()
        self.assertTrue(form.fields['email'].label == None
            or form.fields['email'].label == 'email')

    # The subject field has the correct helper text.
    def test_email_form_char_field_help_text(self):
        form = SubmitQuestionForm()
        self.assertEqual(form.fields['email'].help_text,
            'Optional. Receive notification.')

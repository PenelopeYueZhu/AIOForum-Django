from django.test import TestCase
from django.urls import reverse

from questions.models import Question, Reply, Category
from questions.forms import SubmitQuestionForm

# Class methods for testing lsit of public questions.
class PublicQuestionListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Constants."""
        EVEN_DIVIDER = 2
        NUM_QUESTIONS = 30
        PAGENATE_BY = 10

        """Filler fields."""
        # Create one category just to fill up the questions.
        cat = Category.objects.create(name = 'category 1')
        reply_str_filler = 'This is a filler string for replys. '

        # Create 30 questions
        for question_id in range(NUM_QUESTIONS):
            # First create a reply for the question.
            filler_reply = reply_str_filler + str(question_id)
            # Create a question with filler reply and category.
            question = Question.objects.create(
                subject = str(question_id),
                content = str(question_id) * 3,
                reply = filler_reply,
                op_email = 'yuz@ucsd.edu',
            )
            question.category.add(cat)

            # Every other question, set the status to Public
            if (question_id % EVEN_DIVIDER) == 0:
                question.set_to_public()

            # Save the question.
            question.save()

    # The url exists for list of questions.
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/questions/')
        self.assertEqual(response.status_code, 200)

    # View is accessible by its name.
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    # View is using the right template.
    def test_view_correct_template(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'questions/question_list.html')

    # Pagination.
    def test_pagination_is_ten(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        # First, the page is pagniated.
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        # Then, the pagination is by ten.
        self.assertTrue(len(response.context['question_list']) == 10)

    # View does list all the questions.
    def test_lists_all_questions(self):
        # Get third page where it should have 2 questions listed.
        response = self.client.get(reverse('index')+'?page=2')
        self.assertEqual(response.status_code, 200)
        # First it is paginated.
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        # Then, the page only has 5 questions listed.
        q_left = (30 / 2 ) % 10
        self.assertTrue(len(response.context['question_list']) == q_left)

# Class to test an individual question view.
class QuestionDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up a filler reply and category.
        cat = Category.objects.create(name = 'category 1')
        filler_reply = Reply.objects.create(content = 'This is a reply filler.')

        # Set up the question displayed.
        q = Question.objects.create(
            subject = 'Test question subject 1',
            content = 'Test question content 1',
            reply = filler_reply)
        q.category.add(cat)

    # Url exists for list of questions.
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/questions/test-question-subject-1-1')
        self.assertEqual(response.status_code, 200)

    # View is using the right template.
    def test_view_correct_template(self):
        response = self.client.get('/questions/test-question-subject-1-1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
            'questions/question_detail.html')

class AllQuestionListViewTest(TestCase):
    """All the questions should be listed."""

    @classmethod
    def setUpTestData(cls):
        """Constants."""
        EVEN_DIVIDER = 2
        NUM_QUESTIONS = 31
        PAGENATE_BY = 10

        """Filler fields."""
        # Create one category just to fill up the questions.
        cat = Category.objects.create(name = 'category 1')
        reply_str_filler = 'This is a filler string for replys. '

        # Create 30 questions
        for question_id in range(NUM_QUESTIONS):
            # First create a reply for the question.
            filler_reply = reply_str_filler + str(question_id)
            # Create a question with filler reply and category.
            question = Question.objects.create(
                subject = str(question_id),
                content = str(question_id) * 3,
                reply = filler_reply,
                op_email = 'yuz@ucsd.edu',
        )
        question.category.add(cat)

        # Every other question, set the status to Public to be displayed in
        # View.
        if (question_id % EVEN_DIVIDER) == 0:
            question.set_to_public()

        # Save the question.
        question.save()

    # The url exists for list of questions.
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/questions/youarenotsupposedtobehere')
        self.assertEqual(response.status_code, 200)

    # View is accessible by its name.
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('peaccess'))
        self.assertEqual(response.status_code, 200)

    # View is using the right template.
    def test_view_correct_template(self):
        response = self.client.get(reverse('peaccess'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
            'questions/peeraccess_question_list.html')

    # Pagination.
    def test_pagination_is_ten(self):
        response = self.client.get(reverse('peaccess'))
        self.assertEqual(response.status_code, 200)
        # First, the page is pagniated.
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        # Then, the pagination is by ten.
        self.assertTrue(len(response.context['question_list']) == 10 )

    # View does list all the questions.
    def test_lists_all_questions(self):
        # Get third page where it should have 1 questions listed.
        response = self.client.get(reverse('peaccess')+'?page=4')
        self.assertEqual(response.status_code, 200)
        # First it is paginated.
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        # Then, the page only has 1 questions listed.
        self.assertTrue(len(response.context['question_list']) == 1)

class QuestionByStatusListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """Constants."""
        EVERY_THREE_QUESTION_DIVIDER = 3
        NUM_QUESTIONS = 31
        PAGENATE_BY = 10
        ANSWERED_VIEW = '/questions/youarenotsupposedtobehere/a'

        """Filler fields."""
        # Create one category just to fill up the questions.
        cat = Category.objects.create(name = 'category 1')
        reply_str_filler = 'This is a filler string for replys. '

        # Create 30 questions
        for question_id in range(NUM_QUESTIONS):
            # First create a reply for the question.
            filler_reply = reply_str_filler + str(question_id)
            # Create a question with filler reply and category.
            question = Question.objects.create(
                subject = str(question_id),
                content = str(question_id) * 3,
                reply = filler_reply,
                op_email = 'yuz@ucsd.edu',
            )
            question.category.add(cat)

            # If id is mutiple of 3 + 1, set to answered.
            if (question_id % EVERY_THREE_QUESTION_DIVIDER) == 0:
                question.set_to_answered()

            # if id is multiple of 3 + 2, set the status to public.
            if (question_id % EVERY_THREE_QUESTION_DIVIDER) == 1:
                question.set_to_public()

            # Save the question.
            question.save()

    # The url exists for list of questions with status Answered.
    def test_answered_url_exists_at_desired_location(self):
        response = self.client.get('/questions/youarenotsupposedtobehere/a')
        self.assertEqual(response.status_code, 200)

    # The url exists for list of questions with status Public.
    def test_public_url_exists_at_desired_location(self):
        response = self.client.get('/questions/youarenotsupposedtobehere/p')
        self.assertEqual(response.status_code, 200)

    # The url exists for list of question with status new.
    def test_new_url_exists_at_desired_location(self):
        response = self.client.get('/questions/youarenotsupposedtobehere/n')
        self.assertEqual(response.status_code, 200)

    # View is using the right template.
    def test_view_correct_template(self):
        response = self.client.get('/questions/youarenotsupposedtobehere/a')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
            'questions/peeraccess_question_list.html')

    # Pagination.
    def test_pagination_is_ten(self):
        response = self.client.get('/questions/youarenotsupposedtobehere/a')
        self.assertEqual(response.status_code, 200)
        # First, the page is pagniated.
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        # Then, the pagination is by ten.
        self.assertTrue(len(response.context['question_list']) == 10)

    # View does list all the questions.
    def test_lists_all_answered_questions(self):
        # Get last page of answered questions..
        response = self.client.get('/questions/youarenotsupposedtobehere/a'
            +'?page=2')
        self.assertEqual(response.status_code, 200)
        # First it is paginated.
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        # Then, the page only has 1 questions listed.
        self.assertTrue(len(response.context['question_list']) == 1)

class QuestionEditViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Set up one question to edit."""

        """Filler fields."""
        # Create one category just to fill up the questions.
        cat = Category.objects.create(name = 'category 1')

        # Create a question with filler reply and category.
        question = Question.objects.create(
            subject = 'Test subject for editing.',
            content = 'Test content for editing.',
            reply =  'This is a filler string for replys. ',
            op_email = 'yuz@ucsd.edu',
        )
        question.category.add(cat)
        question.save()

    # Url exists where it should be.
    def test_view_url_exists_at_desired_location(self):
        q_id = Question.objects.first().id
        response = self.client.get('/questions/youarenotsupposedtobehere/'
            +str(q_id)+'/edit')
        self.assertEqual(response.status_code, 200)

    # View using the right template.
    def test_view_correct_template(self):
        q_id = Question.objects.first().id
        response = self.client.get('/questions/youarenotsupposedtobehere/'
            +str(q_id)+'/edit')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'questions/edit_question.html')

# Class to test the subject question form view.
class SubmitQuestionViewTest(TestCase):
    # Url exists for the form.
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/questions/ask')
        self.assertEqual(response.status_code, 200)

    # View accessible by name.
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('submit-question'))
        self.assertEqual(response.status_code, 200)

    # View using the right template.
    def test_view_correct_template(self):
        response = self.client.get(reverse('submit-question'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'questions/submit_question.html')

    # Form is valid.
    def test_form_valid(self):
        # Set up the form.
        form_data = {
            'subject': 'This is a test subject again.',
            'content': 'This is a test content again.',
            'email': 'tet@email.com'}
        # Created form should be valid.
        form = SubmitQuestionForm(data = form_data)
        self.assertTrue(form.is_valid())

    # Form is not valid when there are fields missing.
    def test_form_invalid(self):
        # Set up the form.
        form_data = {
            'subject': '',
            'content': 'This is a test content again.',
            'email': 'tet@email.com'}
        # Created form should be valid.
        form = SubmitQuestionForm(data = form_data)
        self.assertFalse(form.is_valid())

    # View submits a question correctly.
    def test_submit_question(self):
        # Set up the form.
        form_data = {
            'subject': 'This is a test subject again.',
            'content': 'This is a test content again.',
            'email': 'tet@email.com'}

        # Submit the question.
        response = self.client.post('/questions/ask', form_data)

        # Get the submitted question (a private one) and validate it.
        q = Question.objects.get(id=1)
        self.assertEqual(q.slug, 'this-is-a-test-subject-again')
        self.assertEqual(Question.objects.count(), 1)

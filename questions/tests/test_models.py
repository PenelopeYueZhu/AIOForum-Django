from django.test import TestCase

from questions.models import Category, Reply, Question

# Testing Category Model
class CategoryModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Category.objects.create(name = "CategoryTest")

    # 'name' field has label 'name'
    def test_name_label(self):
        # Get the label of category.
        category = Category.objects.get(id=1)
        field_label = category._meta.get_field('name').verbose_name
        # the label is 'name'.
        self.assertEqual(field_label, 'name')

    # 'name' field has max length of 100 words.
    def test_name_max_length(self):
        # Get the max length set for name.
        category = Category.objects.get(id=1)
        max_length = category._meta.get_field('name').max_length
        self.assertEqual(max_length, Category.NAME_MAX_LENGTH)

# Test question model.
class QuestionModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # First set up a reply and a category,
        # since question model has relationship with those two.
        reply_string = """This is a long reply string
            with a second line that is again very very very very very long
            and I am getting tired of writing this much string because
            this is incredibly boring"""
        Category.objects.create(name = "CategoryTest")

        # Set up the question.
        q = Question.objects.create(subject = 'this is a subject line',
            content = 'This is a content line',
            reply = reply_string,
            op_email = 'yuz@ucsd.edu',
            status = 'a')
        q.category.add(Category.objects.get(id=1))

    # subject label.
    def test_subject_label(self):
        # Get 'subject' label.
        q = Question.objects.get(id=1)
        subject_label = q._meta.get_field('subject').verbose_name
        # 'subject' field should have label 'subject'.
        self.assertEqual(subject_label, 'subject')

    # Content label.
    def test_content_label(self):
        # Get 'content' label.
        q = Question.objects.get(id=1)
        label = q._meta.get_field('content').verbose_name
        # 'content' field should have label 'content'.
        self.assertEqual(label, 'content')

    # Reply label.
    def test_reply_label(self):
        # Get 'reply' label.
        q = Question.objects.get(id=1)
        label = q._meta.get_field('reply').verbose_name
        # 'content' field should have label 'reply'.
        self.assertEqual(label, 'reply')

    # Op_email label.
    def test_email_label(self):
        # Get 'op_email' label.
        q = Question.objects.get(id=1)
        label = q._meta.get_field('op_email').verbose_name
        # 'content' field should have label 'op email'.
        self.assertEqual(label, 'op email')

    # Category label.
    def test_content_label(self):
        # Get 'category' label.
        q = Question.objects.get(id=1)
        label = q._meta.get_field('category').verbose_name
        # 'content' field should have label 'cateogyr'.
        self.assertEqual(label, 'category')

    # max_length of subject field.
    def test_subject_max_length(self):
        # Get 'subject' max length.
        q = Question.objects.get(id=1)
        max_length = q._meta.get_field('subject').max_length
        # max length should be 200.
        self.assertEqual(max_length, Question.SUBJECT_MAX_LENGTH)

    # Max_length of content field.
    def test_content_max_length(self):
        # Get 'content' max length.
        q = Question.objects.get(id=1)
        max_length = q._meta.get_field('content').max_length
        # max length should be 200.
        self.assertEqual(max_length, Question.CONTENT_MAX_LENGTH)

    # Max_length of reply field.
    def test_content_max_length(self):
        # Get 'content' max length.
        q = Question.objects.get(id=1)
        max_length = q._meta.get_field('reply').max_length
        # max length should be 200.
        self.assertEqual(max_length, Question.CONTENT_MAX_LENGTH)

    # Absoulte url.
    def test_get_absolute_url(self):
        q = Question.objects.get(id=1)
        self.assertEqual(q.get_absolute_url(),
            '/questions/this-is-a-subject-line-1')

    # Unique slug.
    def test_unique_slug(self):
        # Set up another question that's exactly the same.
        reply_string = """This is a long reply string
            with a second line that is again very very very very very long
            and I am getting tired of writing this much string because
            this is incredibly boring"""

        # Set up the question.
        q = Question.objects.create(subject = 'this is a subject line',
            content = 'This is a content line',
            reply = reply_string,
            op_email = 'yuz@ucsd.edu',
            status = 'a')
        q.category.add(Category.objects.get(id=1))
        q.save()
        # Check if the slug has 0 trailing behind it.
        self.assertEqual(q.slug, 'this-is-a-subject-line-1')
        # Check if the absolute url is different too.
        self.assertEqual(q.get_absolute_url(),
            '/questions/this-is-a-subject-line-1-2')

    # Set functions
    def test_set_functions(self):
        q = Question.objects.get(id=1)
        # public
        q.set_to_public()
        # Now status should be 'p'.
        self.assertEqual(q.status, 'p')

        # answered.
        q.set_to_answered()
        # Now the status should be 'a'.
        self.assertEqual(q.status, 'a')

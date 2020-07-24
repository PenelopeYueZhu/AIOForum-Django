from rest_framework import serializers
from questions.models import Question, Category

class QuestionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('slug', 'subject', 'content', 'post_date', 'reply',
            'category', 'op_email', 'status')

# Generated by Django 3.0.4 on 2020-05-11 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0004_auto_20200511_1610'),
    ]

    operations = [
        migrations.AlterField(
            model_name='privatequestion',
            name='category',
            field=models.ManyToManyField(blank=True, help_text='Select categories applicable for this question', to='questions.Category'),
        ),
        migrations.AlterField(
            model_name='publicquestion',
            name='category',
            field=models.ManyToManyField(blank=True, help_text='Select categories applicable for this question', to='questions.Category'),
        ),
    ]

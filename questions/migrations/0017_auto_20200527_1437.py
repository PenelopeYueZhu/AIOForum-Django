# Generated by Django 3.0.4 on 2020-05-27 19:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0016_auto_20200519_1734'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(default='', max_length=200, unique=True)),
                ('subject', models.CharField(help_text='Summarize your question.', max_length=140)),
                ('content', models.TextField(help_text='State your question here', max_length=1000)),
                ('post_date', models.DateTimeField(auto_now=True)),
                ('op_email', models.EmailField(blank=True, max_length=254)),
                ('category', models.ManyToManyField(blank=True, help_text='Select categories applicable for this question', to='questions.Category')),
                ('reply', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='questions.Reply')),
            ],
            options={
                'ordering': ['-post_date'],
            },
        ),
        migrations.RemoveField(
            model_name='publicquestion',
            name='category',
        ),
        migrations.RemoveField(
            model_name='publicquestion',
            name='reply',
        ),
        migrations.DeleteModel(
            name='PrivateQuestion',
        ),
        migrations.DeleteModel(
            name='PublicQuestion',
        ),
    ]

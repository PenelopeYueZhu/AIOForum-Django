# Generated by Django 3.0.4 on 2020-04-15 20:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0002_publicquestion_op_email'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='privatequestion',
            options={'ordering': ['-post_date']},
        ),
        migrations.AlterModelOptions(
            name='publicquestion',
            options={'ordering': ['-post_date']},
        ),
    ]

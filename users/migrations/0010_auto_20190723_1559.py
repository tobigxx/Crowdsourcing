# Generated by Django 2.1.7 on 2019-07-23 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_textinstruction'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='count',
        ),
        migrations.AddField(
            model_name='question',
            name='mergeParent',
            field=models.IntegerField(default=0),
        ),
    ]

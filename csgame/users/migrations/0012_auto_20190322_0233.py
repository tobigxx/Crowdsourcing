# Generated by Django 2.1.7 on 2019-03-22 02:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_attribute'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagemodel',
            name='label',
            field=models.ManyToManyField(blank=True, related_name='labels', to='users.Label'),
        ),
    ]
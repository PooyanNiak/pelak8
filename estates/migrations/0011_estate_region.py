# Generated by Django 4.0 on 2021-12-22 23:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estates', '0010_estate_elevator'),
    ]

    operations = [
        migrations.AddField(
            model_name='estate',
            name='region',
            field=models.CharField(blank=True, max_length=320, null=True),
        ),
    ]

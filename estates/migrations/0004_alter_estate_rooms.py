# Generated by Django 4.0 on 2021-12-22 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estates', '0003_estate_parking'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estate',
            name='rooms',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]

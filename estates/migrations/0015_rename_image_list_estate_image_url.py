# Generated by Django 4.0 on 2021-12-22 23:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('estates', '0014_estate_image_list'),
    ]

    operations = [
        migrations.RenameField(
            model_name='estate',
            old_name='image_list',
            new_name='image_url',
        ),
    ]
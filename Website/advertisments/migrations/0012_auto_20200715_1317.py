# Generated by Django 3.0.7 on 2020-07-15 07:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('advertisments', '0011_auto_20200713_1308'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='ad_review',
            new_name='ad_message',
        ),
    ]
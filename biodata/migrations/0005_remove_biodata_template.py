# Generated by Django 3.0.2 on 2020-02-04 04:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('biodata', '0004_auto_20200204_0451'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='biodata',
            name='template',
        ),
    ]
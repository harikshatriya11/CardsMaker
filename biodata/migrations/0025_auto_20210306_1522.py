# Generated by Django 2.2.19 on 2021-03-06 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biodata', '0024_auto_20200801_0754'),
    ]

    operations = [
        migrations.AlterField(
            model_name='languagename',
            name='status',
            field=models.IntegerField(choices=[(0, 'ACTIVE'), (1, 'INACTIVE')], default=1),
        ),
    ]
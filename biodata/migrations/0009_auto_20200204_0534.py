# Generated by Django 3.0.2 on 2020-02-04 05:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('biodata', '0008_biodata_template'),
    ]

    operations = [
        migrations.AlterField(
            model_name='biodata',
            name='template',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='biodata_template', to='biodata.TemplateData'),
        ),
    ]
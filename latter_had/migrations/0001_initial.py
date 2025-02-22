# Generated by Django 4.1.5 on 2023-06-22 04:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('languages', '0001_initial'),
        ('cities_light', '0011_alter_city_country_alter_city_region_and_more'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LatterHadTemplateData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('template_name_latterhad', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('template_url_latterhad', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('template_type_latterhad', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('template_price', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('template_image_latterhad_icon', models.ImageField(default='', upload_to='media/latterhad/templates/icon')),
                ('template_image_latterhad', models.ImageField(default='', upload_to='media/latterhad/templates/images')),
                ('status', models.IntegerField(choices=[(0, 'ACTIVE'), (1, 'INACTIVE')], default=0)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('template_country_latterhad', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='template_country_latterhad', to='cities_light.country')),
            ],
        ),
        migrations.CreateModel(
            name='LatterHadCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_name', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('company_name', models.CharField(default='', max_length=100)),
                ('established_date', models.CharField(default='', max_length=100)),
                ('address', models.CharField(default='', max_length=100)),
                ('contact', models.CharField(default='', max_length=100)),
                ('email', models.CharField(default='', max_length=100)),
                ('linkedin', models.CharField(default='', max_length=100)),
                ('website', models.CharField(default='', max_length=100)),
                ('other_social_id', models.CharField(default='', max_length=100)),
                ('facebook', models.CharField(default='', max_length=100)),
                ('twitter', models.CharField(default='', max_length=100)),
                ('latterhad_card_status', models.IntegerField(choices=[(1, 'DRAFT'), (2, 'PUCHASED'), (3, 'WATCHED_ADS'), (4, 'DELETED')], default=1)),
                ('logo', models.ImageField(default='', upload_to='media/resume/templates/images')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='label_language_name', to='languages.latterhad')),
                ('latterhad_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='latterhad_user_details', to='users.userdetails')),
                ('paid_template', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='latter_had.latterhadtemplatedata')),
                ('payment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.payment')),
                ('template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='latterhad_templates', to='latter_had.latterhadtemplatedata')),
            ],
        ),
    ]

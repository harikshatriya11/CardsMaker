# Generated by Django 4.1.5 on 2023-06-22 04:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('languages', '0001_initial'),
        ('cities_light', '0011_alter_city_country_alter_city_region_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='BusinessTemplateData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('template_name_business', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('template_url_business', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('template_type_business', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('template_price', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('template_image_business_icon', models.ImageField(default='', upload_to='media/business/templates/icon')),
                ('template_image_business', models.ImageField(default='', upload_to='media/business/templates/images')),
                ('status', models.IntegerField(choices=[(0, 'ACTIVE'), (1, 'INACTIVE')], default=0)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('template_country_business', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='template_country_business', to='cities_light.country')),
            ],
        ),
        migrations.CreateModel(
            name='BusinessCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_name', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('company_name', models.CharField(default='', max_length=100)),
                ('company_tagline', models.CharField(default='', max_length=100)),
                ('person_name', models.CharField(default='', max_length=100)),
                ('profession', models.CharField(default='', max_length=100)),
                ('established_date', models.CharField(default='', max_length=100)),
                ('address', models.CharField(default='', max_length=100)),
                ('contact', models.CharField(default='', max_length=100)),
                ('telepone', models.CharField(default='', max_length=100)),
                ('email', models.CharField(default='', max_length=100)),
                ('social_id1', models.CharField(default='', max_length=100)),
                ('social_id2', models.CharField(default='', max_length=100)),
                ('website', models.CharField(default='', max_length=100)),
                ('ceo', models.CharField(default='', max_length=100)),
                ('founder', models.CharField(default='', max_length=100)),
                ('business_card_status', models.IntegerField(choices=[(1, 'DRAFT'), (2, 'PUCHASED'), (3, 'WATCHED_ADS'), (4, 'DELETED')], default=1)),
                ('logo', models.ImageField(default='', upload_to='media/business/templates/logo')),
                ('qrcode', models.CharField(default='', max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('business_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='business_user_details', to='users.userdetails')),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='label_language_name', to='languages.business')),
                ('paid_template', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bussiness_cards.businesstemplatedata')),
                ('payment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.payment')),
                ('template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='business_templates', to='bussiness_cards.businesstemplatedata')),
            ],
        ),
    ]
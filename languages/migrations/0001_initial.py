# Generated by Django 4.1.5 on 2023-06-22 04:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LanguageName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_id', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('language_name', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('country_name', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('language_abr', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('status', models.IntegerField(choices=[(0, 'Active'), (1, 'Inactive')], default=1)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Wedding',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label_name', models.TextField(blank=True, default='{}', null=True)),
                ('status', models.IntegerField(choices=[(0, 'Active'), (1, 'Inactive')], default=1)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wedding_languages', to='languages.languagename')),
            ],
        ),
        migrations.CreateModel(
            name='Resume',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label_name', models.TextField(blank=True, default='{}', null=True)),
                ('status', models.IntegerField(choices=[(0, 'Active'), (1, 'Inactive')], default=1)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resume_languages', to='languages.languagename')),
            ],
        ),
        migrations.CreateModel(
            name='LatterHad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label_name', models.TextField(blank=True, default='{}', null=True)),
                ('status', models.IntegerField(choices=[(0, 'Active'), (1, 'Inactive')], default=1)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='latter_had_languages', to='languages.languagename')),
            ],
        ),
        migrations.CreateModel(
            name='Engagement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label_name', models.TextField(blank=True, default='{}', null=True)),
                ('status', models.IntegerField(choices=[(0, 'Active'), (1, 'Inactive')], default=1)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='engagement_languages', to='languages.languagename')),
            ],
        ),
        migrations.CreateModel(
            name='CommonWords',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label_name', models.TextField(blank=True, default='{}', null=True)),
                ('status', models.IntegerField(choices=[(0, 'Active'), (1, 'Inactive')], default=1)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='common_words', to='languages.languagename')),
            ],
        ),
        migrations.CreateModel(
            name='Business',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label_name', models.TextField(blank=True, default='{}', null=True)),
                ('status', models.IntegerField(choices=[(0, 'Active'), (1, 'Inactive')], default=1)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='business_languages_label', to='languages.languagename')),
            ],
        ),
        migrations.CreateModel(
            name='Birthday',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label_name', models.TextField(blank=True, default='{}', null=True)),
                ('status', models.IntegerField(choices=[(0, 'Active'), (1, 'Inactive')], default=1)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='birthday_languages', to='languages.languagename')),
            ],
        ),
        migrations.CreateModel(
            name='Biodata',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label_name', models.TextField(blank=True, default='{}', null=True)),
                ('status', models.IntegerField(choices=[(0, 'Active'), (1, 'Inactive')], default=1)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='biodata_languages', to='languages.languagename')),
            ],
        ),
    ]

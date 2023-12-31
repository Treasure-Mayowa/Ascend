# Generated by Django 4.2.2 on 2023-11-20 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ascend', '0005_alter_youtubecontent_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resources',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.URLField()),
                ('name', models.TextField()),
                ('description', models.TextField()),
                ('url', models.URLField()),
            ],
        ),
    ]

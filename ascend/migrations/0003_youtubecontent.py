# Generated by Django 4.2.2 on 2023-11-15 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ascend', '0002_user_school'),
    ]

    operations = [
        migrations.CreateModel(
            name='YoutubeContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('embed_code', models.TextField()),
                ('source', models.TextField()),
            ],
        ),
    ]
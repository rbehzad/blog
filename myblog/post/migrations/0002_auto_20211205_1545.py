# Generated by Django 3.2.9 on 2021-12-05 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True, max_length=120, null=True, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='category',
            unique_together={('title', 'slug')},
        ),
    ]
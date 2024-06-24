# Generated by Django 4.2.13 on 2024-06-22 11:09

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('News', '0005_alter_author_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='subscribers',
            field=models.ManyToManyField(related_name='subscribed_categories', to=settings.AUTH_USER_MODEL),
        ),
    ]

# Generated by Django 4.2.13 on 2024-06-02 13:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('News', '0002_rename_post_id_comment_post_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='post',
            new_name='comment_post',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='rating',
            new_name='comment_rating',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='text',
            new_name='comment_text',
        ),
    ]

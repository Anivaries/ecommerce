# Generated by Django 4.1.7 on 2023-03-30 18:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0013_userprofile_favorites'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserFavorites',
        ),
    ]

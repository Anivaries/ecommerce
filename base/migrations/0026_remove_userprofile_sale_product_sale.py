# Generated by Django 4.1.7 on 2023-04-04 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0025_userprofile_sale'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='sale',
        ),
        migrations.AddField(
            model_name='product',
            name='sale',
            field=models.BooleanField(default=False),
        ),
    ]

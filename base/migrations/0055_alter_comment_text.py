# Generated by Django 4.1.7 on 2023-04-23 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0054_alter_comment_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.TextField(),
        ),
    ]
# Generated by Django 4.1.7 on 2023-04-05 18:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0027_product_image_code'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='image_code',
            new_name='product_code',
        ),
    ]
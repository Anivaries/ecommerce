# Generated by Django 4.1.7 on 2023-04-18 19:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0045_remove_skincarecategory_sub_category_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='sub_skincare_category',
        ),
    ]

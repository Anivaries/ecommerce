# Generated by Django 4.1.7 on 2023-04-10 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0029_product_front_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='modal_details',
            field=models.TextField(default='Just a short description'),
            preserve_default=False,
        ),
    ]

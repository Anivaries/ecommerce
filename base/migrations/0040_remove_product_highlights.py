# Generated by Django 4.1.7 on 2023-04-16 22:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0039_perfumehighlights_product_highlights'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='highlights',
        ),
    ]

# Generated by Django 4.1.7 on 2023-04-27 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0058_billingaddress_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billingaddress',
            name='city',
            field=models.CharField(blank=True, default='zlatibor', max_length=20),
            preserve_default=False,
        ),
    ]

# Generated by Django 4.1.7 on 2023-04-03 22:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0021_alter_order_coupon'),
    ]

    operations = [
        migrations.RenameField(
            model_name='discountcode',
            old_name='coupon',
            new_name='code',
        ),
    ]

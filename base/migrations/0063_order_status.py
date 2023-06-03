# Generated by Django 4.1.7 on 2023-06-03 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0062_remove_product_sale_product_sale_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Prcss', 'Processing'), ('Cpltd', 'Completed'), ('Cncl', 'Canceled'), ('Hld', 'On Hold'), ('Pndng', 'Pending')], default='Pending', max_length=11),
        ),
    ]

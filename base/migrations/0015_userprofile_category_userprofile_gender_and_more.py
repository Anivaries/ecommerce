# Generated by Django 4.1.7 on 2023-03-31 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0014_delete_userfavorites'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='category',
            field=models.CharField(blank=True, choices=[('P', 'Perfume'), ('J', 'Jewelry')], max_length=10),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female'), ('U', 'Unisex')], max_length=10),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='favorites',
            field=models.ManyToManyField(blank=True, to='base.product'),
        ),
    ]
# Generated by Django 4.1.7 on 2023-04-18 18:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0041_product_highlights'),
    ]

    operations = [
        migrations.CreateModel(
            name='SkinCareCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=20)),
            ],
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(blank=True, choices=[('P', 'Perfume'), ('M', 'Makeup'), ('S', 'Skincare')], max_length=10),
        ),
        migrations.AddField(
            model_name='product',
            name='skincare_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.skincarecategory'),
        ),
    ]

# Generated by Django 5.1 on 2024-08-25 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('texnomart', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]

# Generated by Django 5.1.6 on 2025-04-03 22:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_socialinfo_handle'),
    ]

    operations = [
        migrations.AlterField(
            model_name='socialinfo',
            name='product_infos',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='main.productinfo'),
        ),
    ]

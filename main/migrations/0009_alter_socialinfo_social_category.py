# Generated by Django 5.1.6 on 2025-04-07 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_alter_socialinfo_handle'),
    ]

    operations = [
        migrations.AlterField(
            model_name='socialinfo',
            name='social_category',
            field=models.CharField(choices=[('Facebook', 'facebook'), ('Instagram', 'instagram'), ('Tiktok', 'tiktok'), ('Other', 'other')], default='Instagram', max_length=10),
        ),
    ]

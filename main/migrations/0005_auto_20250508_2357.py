from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_statistic_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='SellerLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.CharField(max_length=50)),
                ('longitude', models.CharField(max_length=50)),
                ('location', models.CharField(default='Dar es salaam', max_length=100)),
                ('user', models.ForeignKey(on_delete=models.CASCADE, related_name='sellerlocation', to='accounts.customuser')),
            ],
        ),
    ]

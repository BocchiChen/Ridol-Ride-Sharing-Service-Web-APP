# Generated by Django 3.2.12 on 2023-02-03 23:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rides', '0009_rideowner_tol_passenger_num'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ridesharer',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rides.rideowner'),
        ),
    ]
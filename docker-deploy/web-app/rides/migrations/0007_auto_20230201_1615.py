# Generated by Django 3.2.12 on 2023-02-01 16:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rides', '0006_ridesharer_owner_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ridesharer',
            name='owner_name',
        ),
        migrations.AddField(
            model_name='ridesharer',
            name='order',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rides.rideowner'),
        ),
    ]

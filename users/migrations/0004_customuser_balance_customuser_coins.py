# Generated by Django 5.2.1 on 2025-05-26 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_delete_emailotp'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=9),
        ),
        migrations.AddField(
            model_name='customuser',
            name='coins',
            field=models.PositiveIntegerField(default=0),
        ),
    ]

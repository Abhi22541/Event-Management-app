# Generated by Django 4.2 on 2023-05-04 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_remove_ticektbooking_bookingid'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticektbooking',
            name='bookingID',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]

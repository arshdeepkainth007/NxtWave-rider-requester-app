# Generated by Django 3.2.16 on 2023-01-09 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RiderApp', '0005_auto_20230108_2335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ridermodel',
            name='Status',
            field=models.CharField(choices=[('X', 'EXPIRED'), ('O', 'CONFIRMED'), ('-', 'PENDING')], default='-', max_length=1),
        ),
    ]

# Generated by Django 3.2.16 on 2023-01-08 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RiderApp', '0004_auto_20230108_2333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ridermodel',
            name='RiderID',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='ridermodel',
            name='Status',
            field=models.CharField(choices=[('O', 'MATCHED'), ('X', 'DELIVERED'), ('-', 'POSTED')], default='-', max_length=1),
        ),
    ]

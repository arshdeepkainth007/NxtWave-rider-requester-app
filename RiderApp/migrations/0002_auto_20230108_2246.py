# Generated by Django 3.2.16 on 2023-01-08 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RiderApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ridermodel',
            name='RequestID',
            field=models.IntegerField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='ridermodel',
            name='Status',
            field=models.CharField(choices=[('X', 'DELIVERED'), ('-', 'POSTED'), ('O', 'MATCHED')], default='-', max_length=1),
        ),
    ]

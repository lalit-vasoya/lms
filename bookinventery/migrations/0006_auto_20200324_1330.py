# Generated by Django 3.0.4 on 2020-03-24 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookinventery', '0005_auto_20200324_1320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='return_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='status',
            field=models.PositiveIntegerField(choices=[('0', 'Pending'), ('1', 'Issue'), ('2', 'Return')], default=0),
        ),
    ]

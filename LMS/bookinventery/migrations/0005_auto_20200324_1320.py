# Generated by Django 3.0.4 on 2020-03-24 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookinventery', '0004_transaction_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='status',
            field=models.CharField(choices=[(0, 'Pending'), (1, 'Issue'), (2, 'Return')], default=0, max_length=1),
        ),
    ]

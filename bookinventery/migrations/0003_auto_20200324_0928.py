# Generated by Django 3.0.4 on 2020-03-24 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookinventery', '0002_auto_20200324_0739'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='return_date',
            field=models.DateField(null=True),
        ),
    ]

# Generated by Django 3.2 on 2021-09-21 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_alter_date_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='date',
            name='date',
            field=models.DateField(default=None, unique=True),
        ),
    ]

# Generated by Django 3.2 on 2021-09-21 21:55

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_alter_date_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='date',
            name='date',
            field=models.DateField(default=uuid.uuid4, unique=True),
        ),
    ]
# Generated by Django 3.2 on 2021-09-29 09:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Date',
            fields=[
                ('id_date', models.BigAutoField(primary_key=True, serialize=False)),
                ('date', models.DateField(default=None, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id_prod', models.BigAutoField(primary_key=True, serialize=False)),
                ('dci', models.CharField(max_length=100)),
                ('dosage', models.CharField(max_length=100)),
                ('forme', models.CharField(max_length=100)),
                ('designation', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ForecastedSales',
            fields=[
                ('id_forcast', models.BigAutoField(primary_key=True, serialize=False)),
                ('quantity', models.IntegerField(default=0)),
                ('model_name', models.CharField(default='auto', max_length=50)),
                ('horizon', models.IntegerField(default=None)),
                ('date', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='forecastsale', to='products.date')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='forecast', to='products.product')),
            ],
            options={
                'unique_together': {('date', 'horizon')},
            },
        ),
        migrations.CreateModel(
            name='AdjustedSales',
            fields=[
                ('id_adjust', models.BigAutoField(primary_key=True, serialize=False)),
                ('quantity', models.IntegerField(default=0)),
                ('date', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.date')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='adjusted', to='products.product')),
            ],
            options={
                'unique_together': {('product', 'date')},
            },
        ),
        migrations.CreateModel(
            name='ActualSales',
            fields=[
                ('id_actual', models.BigAutoField(primary_key=True, serialize=False)),
                ('quantity', models.IntegerField(default=0)),
                ('date', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='actualsale', to='products.date')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='actual', to='products.product')),
            ],
            options={
                'unique_together': {('product', 'date')},
            },
        ),
    ]

# Generated by Django 3.2.3 on 2021-05-31 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CurrencyLastExchange',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_currency', models.CharField(max_length=3, unique=True)),
                ('exchanged_currency', models.CharField(max_length=3, unique=True)),
                ('rate', models.DecimalField(db_index=True, decimal_places=6, max_digits=18)),
            ],
        ),
    ]

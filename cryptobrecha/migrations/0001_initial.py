# Generated by Django 5.0.3 on 2024-03-13 03:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bancos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_no', models.CharField(max_length=255)),
                ('nickname', models.CharField(max_length=255)),
                ('fiat', models.CharField(max_length=3)),
                ('token', models.CharField(max_length=10)),
                ('fecha_hora', models.DateTimeField()),
                ('cantidad', models.IntegerField()),
                ('page', models.CharField(max_length=255)),
                ('bancos', models.CharField(max_length=255)),
                ('pais', models.CharField(max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Comerciante',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=255)),
                ('nickname', models.CharField(max_length=100)),
                ('min_sell_quantity', models.FloatField()),
                ('max_sell_quantity', models.FloatField()),
                ('sell_quantity', models.FloatField()),
                ('price', models.FloatField()),
                ('banks', models.JSONField()),
                ('page', models.CharField(max_length=255)),
                ('activo', models.BooleanField(max_length=255)),
                ('sell_currency', models.CharField(max_length=255)),
                ('buy_currency', models.CharField(max_length=255)),
                ('pais', models.CharField(max_length=255)),
                ('pedidos_mensual', models.FloatField(max_length=255)),
                ('tiempo_de_pago', models.FloatField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Pricing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True)),
                ('stripe_price_id', models.CharField(max_length=50)),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('currency', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('stripe_subscription_id', models.CharField(max_length=50)),
                ('status', models.CharField(max_length=100)),
                ('pricing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', to='cryptobrecha.pricing')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
    ]

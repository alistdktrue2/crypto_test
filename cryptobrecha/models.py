from django.db import models
from django.db.models.fields.related import ForeignKey, ManyToManyField
from django.utils import timezone
from django.shortcuts import reverse
from django.conf import settings
import stripe
from django.contrib.auth.models import User
from allauth.account.signals import email_confirmed
from django.contrib.auth import get_user_model

User = get_user_model()



class Bancos(models.Model):
    user_no = models.CharField(max_length=255)
    nickname = models.CharField(max_length=255)
    fiat = models.CharField(max_length=3)
    token = models.CharField(max_length=10)
    fecha_hora = models.DateTimeField()
    cantidad = models.IntegerField()
    page = models.CharField(max_length=255)
    bancos = models.CharField(max_length=255)
    pais= models.CharField(max_length=10, null=True)
    # Puedes cambiar 'usuarios_bancos' a lo que prefieras

    def __str__(self):
        return f"{self.nickname} - {self.fiat} - {self.token}"

class Comerciante(models.Model):
    user = models.CharField(max_length=255)
    nickname = models.CharField(max_length=100)
    min_sell_quantity = models.FloatField()
    max_sell_quantity = models.FloatField()
    sell_quantity = models.FloatField()
    price = models.FloatField()
    banks = models.JSONField()  # Almacena información bancaria en formato JSON
    page = models.CharField(max_length=255)
    activo = models.BooleanField(max_length=255)
    sell_currency = models.CharField(max_length=255)
    buy_currency = models.CharField(max_length=255)
    pais = models.CharField(max_length=255)
    pedidos_mensual = models.FloatField(max_length=255)
    tiempo_de_pago = models.FloatField(max_length=255)
    


class Pricing(models.Model):
    name= models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    stripe_price_id = models.CharField(max_length=50)
    price = models.DecimalField(decimal_places=2, max_digits=5)
    currency = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pricing = models.ForeignKey(Pricing, on_delete=models.CASCADE, related_name='subscriptions')
    created = models.DateTimeField(auto_now_add=True)
    stripe_subscription_id = models.CharField(max_length=50)
    status = models.CharField(max_length=100)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.user.email

    @property
    def is_active(self):
        return self.status == "active" or self.status == "trialing"



def post_email_confirmed(request, email_address, *args, **kwargs):
    user = User.objects.get(email=email_address.email)
    free_trial_pricing = Pricing.objects.get(name='Free Trial')

    subscription = Subscription.objects.create(
        user=user,
        pricing=free_trial_pricing
    )

    #Crear cliente en stripe
    stripe_customer = stripe.Customer.create(
        email=user.email
    )

    stripe_subscription = stripe.Subscription.create(
        customer=stripe_customer["id"],
        items=[{'price': 'price_1HAFmwA2yg3TLgLvda4AwmQb'}],
        trial_period_days=7
    )

    subscription.status=stripe_subscription["status"]
    subscription.stripe_subscription_id = stripe_subscription["id"]
    subscription.save()
    user.stripe_customer_id=stripe_customer["id"]
    user.save()


email_confirmed.connect(post_email_confirmed)
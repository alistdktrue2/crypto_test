from rest_framework import serializers
from .models import Buyer, Vendor

class BuyerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Buyer
        fields = '__all__'

class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'
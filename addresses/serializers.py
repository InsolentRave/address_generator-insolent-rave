# coding: utf-8

from rest_framework import serializers

from .models import Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        exclude = ["path"]


class CreateAddressRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        exclude = ["address"]

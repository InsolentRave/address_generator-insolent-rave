# coding: utf-8

import logging

from django.db import models

from .address_generator import generate_address

logger = logging.getLogger('django')


class Address(models.Model):
    currency = models.CharField(max_length=3, help_text='three-letter acronym, such as “BTC” or “ETH”')
    address = models.CharField(max_length=100)
    path = models.CharField(max_length=100, help_text='path of the key hierarchy')

    @classmethod
    def create(cls, currency, path):
        address = generate_address(currency, path)

        logger.info("Creating address; currency='%s' address='%s'", currency, address)

        instance = cls(currency=currency, path=path, address=address)
        instance.save()

        return instance

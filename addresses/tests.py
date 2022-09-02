from multiprocessing.sharedctypes import Value
from unittest.mock import ANY, patch

from django.conf import settings
from django.test import TestCase

from .address_generator import generate_address
from .errors import NotSupportedCurrency, PrivateKeyError


class TestAddressGenerator(TestCase):
    @patch('addresses.address_generator.BIP32HDWallet')
    def test_address_is_derived_from_xprivate_key(self, wallet):
        path = 'm/1/2/3'
        generate_address('BTC', path)

        wallet.return_value.from_xprivate_key.assert_called_once_with(
            xprivate_key=settings.ZEPLY_XPRIVATE_KEY,
            strict=True
        )

        wallet.return_value.from_path.assert_called_once_with(path)

    def test_error_when_currency_is_not_supported(self):
        with self.assertRaises(NotSupportedCurrency):
            generate_address('USD', 'm/1/2/3')


    @patch('addresses.address_generator.BIP32HDWallet')
    def test_error_when_private_key_is_not_valid(self, wallet):
        wallet.return_value.from_xprivate_key.side_effect = ValueError()

        with self.assertRaises(PrivateKeyError):
            generate_address('BTC', 'm/1/2/3')

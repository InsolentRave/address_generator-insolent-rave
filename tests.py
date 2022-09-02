from unittest.mock import ANY

from django.conf import settings
from django.test import Client, TestCase

from addresses.models import Address


class TestAddressesEndpoints(TestCase):
    def setUp(self):
        self.client = Client()
        settings.ZEPLY_XPRIVATE_KEY = \
            'xprv9s21ZrQH143K24t96gCaezzt1QQmnqiEGm8m6TP8yb8e3TmGfkC' \
            'gcLEVsskufMW9R4KH27pD1kyyEfJkYz1eiPwjhFzB4gtabH3PzMSmXSM'

    def test_create_address_returns_address_and_id(self):
        response = self.client.post('/addresses/', {"currency": "BTC", "path": "m/44/1/0/3"})

        self.assertIn("id", response.json())
        self.assertEqual(response.json()["address"], '1CC83aj4zdaTxhtfoZ6Ahs7KtYmDzFwzsj')
        self.assertEqual(response.status_code, 201)

    def test_retrieve_address_returns_only_non_sensitive_data(self):
        Address.create(currency="ETH", path="m/1/2/3")

        response = self.client.get('/addresses/1/')

        self.assertEqual(
            response.json(),
            {
                "id": 1,
                "currency": "ETH",
                "address": "0x49846531f6ce6f54000c57fBAcd35b38DB18846c",
            }
        )

        self.assertEqual(response.status_code, 200)

    def test_list_returns_list_of_public_data(self):
        Address.create(currency="ETH", path="m/0/2/0")
        Address.create(currency="BTC", path="m/1/1/0")

        response = self.client.get('/addresses/')

        self.assertEqual(
            response.json(),
            [
                {
                    "id": ANY,
                    "currency": "ETH",
                    "address": "0x25977dc803298Ca3F5B94D88a22Aeb38dd8485c9",
                },
                {
                    "id": ANY,
                    "currency": "BTC",
                    "address": "18CWL65tjPRhkJUDqdNssMrhKCiKrN6iRC",
                },
            ]
        )

        self.assertNotEqual(response.json()[0]["id"], response.json()[1]["id"])

        self.assertEqual(response.status_code, 200)

    def test_create_returns_bad_request_when_currency_is_not_supported(self):
        response = self.client.post('/addresses/', {"currency": "USD", "path": "m/44/1/0/3"})

        self.assertIn('Non supported currency', response.json()["detail"])
        self.assertEqual(response.status_code, 400)

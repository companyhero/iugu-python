import unittest

from iugu.config import Config
from iugu.errors import ApiError
from iugu.handlers.customer_handler import CustomerHandler
from iugu.http_client.fake_http_client import FakeHttpClient


class ListPaymentMethodsTest(unittest.IsolatedAsyncioTestCase):
    async def test_returns_payment_methods_list(self) -> None:
        payload = [
            {
                "id": "PM1",
                "description": "Meu Cartão",
                "item_type": "credit_card",
                "customer_id": "IUGU-CUSTOMER",
                "data": {"brand": "Visa", "display_number": "XXXX-XXXX-XXXX-1111"},
            }
        ]
        http_client = FakeHttpClient(output_payload=payload)
        handler = CustomerHandler(http_client=http_client, config=Config(api_key="test"))

        result = await handler.list_payment_methods("IUGU-CUSTOMER")

        self.assertTrue(http_client.get_called)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["id"], "PM1")

    async def test_unwraps_items_payload(self) -> None:
        http_client = FakeHttpClient(
            output_payload={"items": [{"id": "PM2", "item_type": "credit_card"}]}
        )
        handler = CustomerHandler(http_client=http_client, config=Config(api_key="test"))

        result = await handler.list_payment_methods("IUGU-CUSTOMER")

        self.assertEqual(result[0]["id"], "PM2")

    async def test_empty_dict_means_no_payment_methods(self) -> None:
        http_client = FakeHttpClient(output_payload={})
        handler = CustomerHandler(http_client=http_client, config=Config(api_key="test"))

        result = await handler.list_payment_methods("IUGU-CUSTOMER")

        self.assertEqual(result, [])

    async def test_raises_on_errors_payload(self) -> None:
        http_client = FakeHttpClient(output_payload={"errors": "Customer Not Found"})
        handler = CustomerHandler(http_client=http_client, config=Config(api_key="test"))

        with self.assertRaises(ApiError):
            await handler.list_payment_methods("missing")


if __name__ == "__main__":
    unittest.main()

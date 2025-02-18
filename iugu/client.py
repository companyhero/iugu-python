from iugu.handlers.customer_handler import CustomerHandler
from iugu.handlers.invoice_handler import InvoiceHandler
from iugu.http_client.httpx_client import HttpxClient
from iugu.http_client.protocols import HttpClient

from .config import Config


class Client:
    def __init__(
        self,
        api_key: str,
        http_client: HttpClient = HttpxClient(),
    ) -> None:
        self._config = Config(api_key=api_key)
        self._http_client = http_client

    @property
    def api_key(self) -> str:
        return self._config.api_key

    @property
    def customer(self) -> CustomerHandler:
        return CustomerHandler(http_client=self._http_client, config=self._config)

    @property
    def invoice(self) -> InvoiceHandler:
        return InvoiceHandler(http_client=self._http_client, config=self._config)

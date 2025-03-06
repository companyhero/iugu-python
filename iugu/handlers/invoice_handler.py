from iugu.errors import ApiError
from iugu.handlers.base_handler import BaseHandler
from iugu.http_client.http_response import HttpResponse
from iugu.invoice import Invoice


class InvoiceHandler(BaseHandler):
    @property
    def base_endpoint(self) -> str:
        return "/v1/invoices/"

    async def create_invoice(self, invoice: Invoice) -> HttpResponse:
        output = await self.request(
            method="post",
            url=self._config.get_environ_url() + self.base_endpoint,
            json=invoice.asdict(),
        )
        if "errors" in output.json:
            raise ApiError(output.json.get("errors", "unknow error"))
        return output

    async def cancel_bill(self, id: str) -> HttpResponse:
        output = await self.request(
            method="put",
            url=f"{self._config.get_environ_url()}{self.base_endpoint}{id}/cancel")
        if "errors" in output.json:
            raise ApiError(output.json.get("errors", "unknow error"))
        return output

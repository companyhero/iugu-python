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


    async def charge_invoice(self, invoice: Invoice, credit_card_token: str = "", payment_profile_id: str = "") -> HttpResponse:
        payload = {
          "invoice_id": invoice.id
        }
        if credit_card_token:
            payload["token"] = credit_card_token
        if payment_profile_id:
            payload["customer_payment_method_id"] = payment_profile_id
        ENDPOINT = "/v1/charge"
        output = await self.request(
            method="post",
            url=self._config.get_environ_url() + ENDPOINT,
            json=payload,
        )
        if "errors" in output.json:
            raise ApiError(output.json.get("errors", "unknow error"))
        return output


    async def create_and_charge_invoice(self, invoice: Invoice, credit_card_token: str = "", payment_profile_id: str = "") -> HttpResponse:
        payload = {
          "months": invoice.max_installments_value,
          "method": invoice.payable_with,
          "restrict_payment_method": True,
          "customer_id": invoice.customer.id,
          "email": invoice.customer.email,
          "discount_cents": invoice.discount_cents,
          "bank_slip_extra_days": 3,
          "keep_dunning": True,
          "items": [item.asdict() for item in invoice.items],
          "payer": {
              "cpf_cnpj": invoice.customer.documentation,
              "name": invoice.customer.name,
              "email": invoice.customer.email,
              "address": {
                  "zip_code": invoice.customer.address.zipcode,
                  "street": invoice.customer.address.street,
                  "number": invoice.customer.address.number,
                  "district": invoice.customer.address.neighborhood,
                  "city": invoice.customer.address.city,
                  "state": invoice.customer.address.state,
                  "complement": invoice.customer.address.complement,
              },
          },
          # "soft_descriptor_light": "descrição_da_cobrança"
        }
        if invoice.subscription_id:
            payload["order_id"] = invoice.subscription_id
        if credit_card_token:
            payload["token"] = credit_card_token
        if payment_profile_id:
            payload["customer_payment_method_id"] = payment_profile_id
        ENDPOINT = "/v1/charge"
        output = await self.request(
            method="post",
            url=self._config.get_environ_url() + ENDPOINT,
            json=payload,
        )
        if "errors" in output.json:
            raise ApiError(output.json.get("errors", "unknow error"))
        return output

    async def cancel_invoice(self, id: str) -> HttpResponse:
        """https://api.iugu.com/v1/invoices/{id}/cancel"""
        output = await self.request(
            method="put",
            url=self._config.get_environ_url() + self.base_endpoint + id + "/cancel",
            json={},
        )
        if "errors" in output.json:
            raise ApiError(output.json.get("errors", "unknow error"))
        return output

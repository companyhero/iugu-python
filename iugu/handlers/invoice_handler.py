from iugu.errors import ApiError
from iugu.handlers.base_handler import BaseHandler
from iugu.http_client.http_response import HttpResponse
from iugu.invoice import Invoice


class InvoiceHandler(BaseHandler):
    @property
    def base_endpoint(self) -> str:
        return "/v1/invoices/"

    async def create_invoice(self, invoice: Invoice) -> HttpResponse:
        return await self.request(
            method="post",
            url=self._config.get_environ_url() + self.base_endpoint,
            json=invoice.asdict(),
        )

    async def charge_invoice(self, invoice: Invoice, credit_card_token: str = "", payment_profile_id: str = "") -> HttpResponse:
        payload = {
          "invoice_id": invoice.id
        }
        assert not (credit_card_token and payment_profile_id), "choose between credit_card_token or customer_payment_method_id"
        if credit_card_token:
            payload["token"] = credit_card_token
        if payment_profile_id:
            payload["customer_payment_method_id"] = payment_profile_id
        ENDPOINT = "/v1/charge"
        return await self.request(
            method="post",
            url=self._config.get_environ_url() + ENDPOINT,
            json=payload,
        )


    async def create_and_charge_invoice(self, invoice: Invoice, credit_card_token: str = "", payment_profile_id: str = "") -> HttpResponse:
        payload = {
          "months": invoice.max_installments_value,
          "method": "bank_slip",
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
        assert not (credit_card_token and payment_profile_id), "choose between credit_card_token or customer_payment_method_id"
        if invoice.subscription_id:
            payload["order_id"] = invoice.subscription_id
        if credit_card_token:
            payload["token"] = credit_card_token
            del payload["method"]
        if payment_profile_id:
            payload["customer_payment_method_id"] = payment_profile_id
            del payload["method"]
        print(payload)
        ENDPOINT = "/v1/charge"
        return await self.request(
            method="post",
            url=self._config.get_environ_url() + ENDPOINT,
            json=payload,
        )

    async def cancel_invoice(self, id: str) -> HttpResponse:
        """https://api.iugu.com/v1/invoices/{id}/cancel"""
        return await self.request(
            method="put",
            url=self._config.get_environ_url() + self.base_endpoint + id + "/cancel",
            json={},
        )
    
    async def refund_invoice(self, invoice_id: str, amount: float) -> HttpResponse:
        """
        Realiza o reembolso de uma fatura no IUGU.

        :param invoice_id: ID da fatura que será reembolsada
        :param amount: Valor a ser reembolsado (obrigatório)
        :return: HttpResponse com o status da operação
        """
        # Validação do valor
        if amount <= 0:
            raise ValueError("O valor de reembolso deve ser maior que zero.")
        
        payload = {
            "amount": amount
        }

        return await self.request(
            method="post",
            url=self._config.get_environ_url() + self.base_endpoint + invoice_id + "/refund",
            json=payload,
        )

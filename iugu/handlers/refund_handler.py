from iugu.handlers.base_handler import BaseHandler
from iugu.http_client.http_response import HttpResponse


class RefundHandler(BaseHandler):
    @property
    def base_endpoint(self) -> str:
        return "/v1/invoices/"

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

from iugu.handlers.refund_handler import RefundHandler
from iugu.http_client.protocols import HttpClientProtocol


class Refund:
    
    def __init__(self, client: HttpClientProtocol):
        self.client = client
        self.handler = RefundHandler(client)

    async def refund(self, invoice_id: str, amount: float | None = None):
        
        response = await self.handler.refund_invoice(invoice_id, amount)
        return response

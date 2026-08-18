from typing import Any

from iugu.address import Address
from iugu.customer import Customer
from iugu.errors import ApiError
from iugu.handlers.base_handler import BaseHandler


class CustomerHandler(BaseHandler):
    @property
    def base_endpoint(self) -> str:
        return "/v1/customers/"

    async def create_customer(self, customer: Customer) -> Any:
        output = await self.request(
            method="post",
            url=self._config.get_environ_url() + self.base_endpoint,
            json=customer.asdict(),
        )
        if "errors" in output.json:
            raise ApiError(output.json.get("errors", "unknow error"))
        return output

    async def update_customer(self, customer: Customer, id: int) -> Any:
        url = f"{self._config.get_environ_url()}{self.base_endpoint}{id}"
        customer_asdict = customer.asdict()
        del customer_asdict["email"]
        output = await self.request(
            method="put",
            url=url,
            json=customer_asdict,
        )
        if "errors" in output.json:
            raise ApiError(output.json.get("errors", "unknow error"))
        return output

    async def delete_customer(self, id: int) -> Any:
        url = f"{self._config.get_environ_url()}{self.base_endpoint}{id}"
        output = await self.request(method="delete", url=url, json=None)
        if "errors" in output.json:
            output.json = {"id": id}
            return output
        return output

    async def list_customers(
        self,
        start: int = 0,
        limit: int = 100,
        created_at_from: str = "",
        created_at_to: str = "",
        updated_since: str = "",
        query: str = "",
    ) -> Any:
        # TODO: raise when it receive errors
        # ?limit=limit&start=start&created_at_from=created_at_from&created_at_to=created_at_to&query=query&updated_since=updated_since"
        url = (
            f"{self._config.get_environ_url()}"
            f"{self.base_endpoint}?limit={limit}&start={start}"
        )
        if created_at_from:
            url += f"&created_at_from={created_at_from}"
        if created_at_to:
            url += f"&created_at_to={created_at_to}"
        if query:
            url += f"&query={query}"
        if updated_since:
            updated_since += f"&updated_since={updated_since}"
        output = await self.request(method="get", url=url)
        if "error" in output.json:
            raise ApiError(output.json.get("error", "unknow error"))
        raw_customers = output.json.get("items", [])
        print(raw_customers)
        customers: list[Customer] = []
        for c in raw_customers:
            customer = Customer(
                name=c.get("name"),
                email=c.get("email"),
                documentation=c.get("cpf_cnpj"),
                default_payment_method_id=c.get("default_payment_method_id", ""),
                notes=c.get("notes", "Finance Integration for Iugu"),
                id=c.get("id", ""),
                updated_at=c.get("updated_at", ""),
                address=Address(
                    street=c.get("street"),
                    state=c.get("state"),
                    neighborhood=c.get("district"),
                    city=c.get("city"),
                    zipcode=c.get("zip_code"),
                    complement=c.get("complement"),
                    number=c.get("number"),
                ),
            )
            customers.append(customer)
        return customers

    async def create_payment_method(
        self,
        customer_id: str,
        token: str,
        description: str = "Cartão de crédito",
        set_as_default: bool = True,
    ) -> Any:
        """Attach a tokenized card as a customer payment method.

        Uses Iugu endpoint POST /v1/customers/{customer_id}/payment_methods.
        See: https://dev.iugu.com/reference/criar-forma-de-pagamento
        """
        url = (
            f"{self._config.get_environ_url()}"
            f"{self.base_endpoint}{customer_id}/payment_methods"
        )
        output = await self.request(
            method="post",
            url=url,
            json={
                "description": description,
                "token": token,
                "set_as_default": set_as_default,
            },
        )
        if "errors" in output.json:
            raise ApiError(output.json.get("errors", "unknown error"))
        return output

    async def list_payment_methods(self, customer_id: str) -> list[Any]:
        """List payment methods for an Iugu customer.

        Uses Iugu endpoint GET /v1/customers/{customer_id}/payment_methods.
        See: https://dev.iugu.com/reference/listar-forma-de-pagamento
        """
        url = (
            f"{self._config.get_environ_url()}"
            f"{self.base_endpoint}{customer_id}/payment_methods"
        )
        output = await self.request(method="get", url=url)
        return self._normalize_payment_methods_payload(output.json)

    @staticmethod
    def _normalize_payment_methods_payload(payload: Any) -> list[Any]:
        """Iugu returns a list, {items: [...]}, or {} when the customer has no cards."""
        if not payload:
            return []
        if isinstance(payload, list):
            return payload
        if isinstance(payload, dict):
            errors = payload.get("errors")
            if errors:
                raise ApiError(errors)
            items = payload.get("items") or payload.get("payment_methods") or []
            return items if isinstance(items, list) else []
        return []

    async def create_payment_profile(
        self, gateway_token: str, customer_id: str, payment_method_code: str
    ) -> Any:
        base_endpoint = "/v1/payment_profiles"
        output = await self.request(
            method="post",
            url=self._config.get_environ_url() + base_endpoint,
            json={
                "gateway_token": gateway_token,
                "customer_id": customer_id,
                "payment_method_code": payment_method_code,
            },
        )
        if "errors" in output.json:
            raise ApiError(output.json.get("errors", "unknown error"))
        return output

    async def get_client(self, id: str) -> Any:
        url = f"{self._config.get_environ_url()}{self.base_endpoint}{id}"
        output = await self.request(method="get", url=url)
        if "errors" in output.json:
            raise ApiError(output.json.get("errors", "unknow error"))
        return output

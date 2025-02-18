from dataclasses import dataclass
from typing import Literal

from iugu.address import Address
from iugu.custom_var import CustomVar


@dataclass
class Customer:
    name: str
    email: str
    documentation: str
    address: Address
    notes: str = "Finance Integration for Iugu"
    id: str = ""

    def __post_init__(self) -> None:
        self._phone: dict[str, str] = {}
        self._custom_vars: dict[str, CustomVar] = {}
        self._status: Literal["active", "inactive"]

    def add_phone(self, prefix: str, number: str) -> None:
        self._phone = {"prefix": prefix, "number": number}

    def add_custom_var(self, name: str, value: str) -> None:
        self._custom_vars[name] = CustomVar(name=name, value=value)

    def asdict(self) -> dict[str, str | list[dict[str, dict[str, str]]]]:
        repr = {
            "email": self.email,
            "name": self.name,
            "notes": self.notes,
            "cpf_cnpj": self.documentation,
            "cc_emails": "",
            "zip_code": self.address.zipcode,
            "number": self.address.number,
            "street": self.address.street,
            "city": self.address.city,
            "state": self.address.state,
            "district": self.address.neighborhood,
            "complement": self.address.complement,
        }
        repr.update(self._phone)
        if self._custom_vars:
            repr["custom_variables"] = [
                var.asdict() for var in self._custom_vars.values()
            ]
        return repr

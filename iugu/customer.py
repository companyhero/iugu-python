from dataclasses import dataclass
from typing import Literal

from iugu.address import Address


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
        self._status: Literal["active", "inactive"]

    def add_phone(self, prefix: str, number: str) -> None:
        self._phone = {"prefix": prefix, "number": number}

    def set_status(self, status: Literal["active", "inactive"]) -> None:
        self._status = status

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
            "custom_variables": [
                # {"name": "asdf", "value": "asdf"},
            ],
        }
        repr.update(self._phone)
        return repr

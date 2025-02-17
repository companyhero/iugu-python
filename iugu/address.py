from dataclasses import dataclass


@dataclass
class Address:
    street: str
    neighborhood: str
    state: str
    city: str
    zipcode: str
    complement: str
    number: str = "SN"
    country: str = "BR"

    def asdict(self) -> dict[str, str]:
        return {
            "street": self.street,
            "state": self.state,
            "neighborhood": self.neighborhood,
            "city": self.city,
            "zipcode": self.zipcode,
            "complement": self.complement,
            "number": self.number,
            "country": self.country,
        }

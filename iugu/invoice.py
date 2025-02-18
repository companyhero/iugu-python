from dataclasses import dataclass, field
from datetime import date

from iugu.customer import Customer


@dataclass
class InvoiceItem:
    description: str
    quantity: int
    amount: int | float

    @property
    def price_cents(self) -> int:
        return int(self.amount * 100)

    def asdict(self) -> dict[str, str]:
        return {
            "description": self.description,
            "quantity": str(self.quantity),
            "price_cents": self.price_cents,
        }


@dataclass
class Invoice:
    due_date: date
    customer: Customer
    ensure_workday_due_date: bool = True
    expires_in: str = "0"
    bank_slip_extra_due: str = "1"
    cc_emails: list[str] = field(default_factory=list)
    payable_with: list[str] = field(
        default_factory=lambda: ["credit_card", "pix", "bank_slip"]
    )
    subscription_id: str | None = None
    ignore_canceled_email: bool = True
    discount_cents: str | None = None
    ignore_due_email: bool = False
    order_id: str | None = None
    external_reference: str | None = None
    max_installments_value: int = 12
    email: str = ""
    id: str = ""

    def __post_init__(self) -> None:
        self.items: list[InvoiceItem] = []

    def add_item(self, description: str, quantity: int, amount: int | float) -> None:
        item = InvoiceItem(description=description, quantity=quantity, amount=amount)
        self.items.append(item)

    def asdict(self) -> dict[str, dict[str, str] | str]:
        invoice_dict = {
            "email": self.email or self.customer.email,
            "cc_emails": ",".join(self.cc_emails),
            "due_date": self.due_date.isoformat(),
            "ensure_workday_due_date": self.ensure_workday_due_date,
            "expires_in": self.expires_in,
            "bank_slip_extra_due": self.bank_slip_extra_due,
            "items": [item.asdict() for item in self.items],
            "payable_with": self.payable_with,
            "payer": {
                "cpf_cnpj": self.customer.documentation,
                "name": self.customer.name,
                "email": self.customer.email,
                "address": {
                    "zip_code": self.customer.address.zipcode,
                    "street": self.customer.address.street,
                    "number": self.customer.address.number,
                    "district": self.customer.address.neighborhood,
                    "city": self.customer.address.city,
                    "state": self.customer.address.state,
                    "complement": self.customer.address.complement,
                },
            },
            "ignore_canceled_email": self.ignore_canceled_email,
            "ignore_due_email": self.ignore_due_email,
            "max_installments_value": self.max_installments_value,
        }
        optional_fields = {
            "customer_id": self.customer.id,
            "subscription_id": self.subscription_id,
            "discount_cents": self.discount_cents,
            "order_id": self.order_id,
            "external_reference": self.external_reference,
        }
        for key, value in optional_fields.items():
            if value is not None:
                invoice_dict[key] = value
        if hasattr(self.customer, "_phone"):
            invoice_dict["payer"]["phone_prefix"] = self.customer._phone.get(
                "prefix", ""
            )
            invoice_dict["payer"]["phone"] = self.customer._phone.get("number", "")
        return invoice_dict

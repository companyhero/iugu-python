from dataclasses import dataclass


@dataclass
class CustomVar:
    name: str
    value: str

    def asdict(self) -> dict[str, str]:
        return {"name": self.name, "value": self.value}

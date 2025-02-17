from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    api_key: str

    def get_environ_url(self) -> str:
        return "https://api.iugu.com"

    def get_api_key(self) -> str:
        return self.api_key

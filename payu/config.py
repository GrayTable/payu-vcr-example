from pydantic import BaseModel


class PayUConfig(BaseModel):
    grant_type: str = "client_credentials"
    client_id: int
    client_secret: str
    enable_sandbox: bool
    api_version: str = "v2_1"
    sandbox_url: str = "https://secure.snd.payu.com"
    prod_url: str = "https://secure.payu.com"


class PayUUrls(BaseModel):
    base_url: str
    api_url: str

    @classmethod
    def build_from_config(cls, config: PayUConfig):
        base_url = config.enable_sandbox and config.sandbox_url or config.prod_url
        api_url = f"{base_url}/api/{config.api_version}"

        return cls(
            base_url=base_url,
            api_url=api_url,
        )

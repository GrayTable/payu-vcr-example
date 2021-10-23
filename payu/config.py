from pydantic import BaseModel


class PayUConfig(BaseModel):
    grant_type: str = "client_credentials"
    client_id: int
    client_secret: str
    enable_sandbox: bool
    api_version: str = "v2_1"

    sandbox_url: str = "https://secure.snd.payu.com"
    prod_url: str = "https://secure.payu.com"


class PayUResourceUrls(BaseModel):
    auth: str
    order_list: str
    order_detail: str
    order_status: str
    order_refunds: str
    order_transactions: str

    @classmethod
    def build_from_config(cls, config: PayUConfig):
        base_url = config.enable_sandbox and config.sandbox_url or config.prod_url
        base_api_url = f"{base_url}/api/{config.api_version}"

        auth = f"{base_url}/pl/standard/user/oauth/authorize"

        order_list = base_api_url + "/orders"
        order_detail = order_list + "/{order_id}"
        order_status = order_detail + "/status"
        order_refunds = order_detail + "/refunds"
        order_transactions = order_detail + "/transactions"

        return cls(
            auth=auth,
            order_list=order_list,
            order_detail=order_detail,
            order_status=order_status,
            order_refunds=order_refunds,
            order_transactions=order_transactions,
        )

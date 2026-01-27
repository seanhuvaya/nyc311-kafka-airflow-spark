from typing import Optional, Dict

from requests.adapters import HTTPAdapter
from urllib3 import Retry

from src.base_client import BaseAPIClient
from src.config import Config


class ResilientAPIClient(BaseAPIClient):
    def __init__(
            self,
            base_url: str,
            headers: Optional[Dict[str, str]] = None,
            timeout: int = Config.REQUEST_TIMEOUT,
    ):
        super().__init__(base_url, headers, timeout)

        retries = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"],
        )

        adapter = HTTPAdapter(max_retries=retries)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

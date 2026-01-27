from enum import Enum
from typing import Optional, Dict, Any

import requests

from src.config import Config


class HttpMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"

class APIClientError(Exception):
    pass

class BaseAPIClient:
    def __init__(
            self,
            base_url: str,
            headers: Optional[Dict[str, str]] = None,
            timeout: int = Config.REQUEST_TIMEOUT
    ):
        self.base_url = base_url.rstrip("/")
        self.headers = headers or {}
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def _request(
            self,
            method: str,
            endpoint: str,
            params: Optional[Dict[str, Any]] = None,
            json: Optional[Dict[str, Any]] = None,
    ):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = self.session.request(
            method,
            url,
            params=params,
            json=json,
            timeout=self.timeout,
        )

        if not response.ok:
            raise APIClientError(
                f"{method} {endpoint} failed [{response.status_code}]: {response.text}"
            )

        return response.json()

    def get(
            self,
            endpoint: str,
            params: Optional[Dict[str, Any]] = None,
    ):
        return self._request(HttpMethod.GET.value, endpoint, params=params)

    def post(
            self,
            endpoint: str,
            params: Optional[Dict[str, Any]] = None,
            json: Optional[Dict[str, Any]] = None,
    ):
        return self._request(HttpMethod.POST.value, endpoint, params=params, json=json)

    def put(
            self,
            endpoint: str,
            params: Optional[Dict[str, Any]] = None,
            json: Optional[Dict[str, Any]] = None,
    ):
        return self._request(HttpMethod.PUT.value, endpoint, params=params, json=json)

    def delete(
            self,
            endpoint: str,
            params: Optional[Dict[str, Any]] = None,
    ):
        return self._request(HttpMethod.DELETE.value, endpoint, params=params)




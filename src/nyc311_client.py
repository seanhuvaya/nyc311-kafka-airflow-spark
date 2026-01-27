from src.config import Config
from src.resilient_client import ResilientAPIClient


class NYC311_Client(ResilientAPIClient):
    def __init__(self, app_token: str):
        super().__init__(
            base_url=Config.API_BASE_URL,
            headers={
                "X-App-Token": app_token,
                "Accept": "application/json"
            }
        )

    def get_complaints(
            self,
            start_date: str,
            end_date: str,
            limit: int = 1000,
            offset: int = 0
    ):
        params = {
            "$select": ("unique_key,created_date,closed_date,agency,agency_name,complaint_type,descriptor,",
                        "incident_zip,borough,status,open_data_channel_type,latitude,longitude"),
            "$where": f"created_date BETWEEN '{start_date}' AND '{end_date}'",
            "$order": "created_date ASC",
            "$limit": limit,
            "$offset": offset
        }

        return self.get("erm2-nwe9", params=params)

import requests
from .config import BASE_API, API_TIMEOUT


class ApiClient:

    def notify_transfer_complete(self, mission_name):

        url = f"{BASE_API}/mission_uploaded"

        data = {
            "mission": mission_name
        }

        try:
            requests.post(url, json=data, timeout=API_TIMEOUT)
        except Exception:
            pass
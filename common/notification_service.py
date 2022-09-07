import json
import logging
import requests

logger = logging.getLogger(__name__)


def _prepare_sms_payload(sender, destinations, text):
    destinations_data = []
    for d in destinations:
        destinations_data.append({"destination": d, "format": "mobile"})
    return json.dumps({"sender": sender, "to": destinations_data, "text": text})


class NotificationService:
    SEND_SMS_ENDPOINT = "message/send"
    CONNECTION_TIMEOUT = 10

    def __init__(self, api_token, api_url) -> None:
        self.api_token = api_token
        self.api_url = api_url
        super().__init__()

    def send_sms(self, sender, destinations, text):
        data = _prepare_sms_payload(sender, destinations, text)
        url = f"{self.api_url}{self.SEND_SMS_ENDPOINT}"
        headers = {
            "Authorization": "Token " + self.api_token,
            "Content-Type": "application/json",
        }

        try:
            response = requests.post(
                url, data=data, headers=headers, timeout=self.CONNECTION_TIMEOUT
            )

            response.raise_for_status()
        except requests.exceptions.HTTPError:
            logger.exception("SMS message sent failed!")

        return response

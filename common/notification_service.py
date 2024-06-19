import json
import logging
import requests

logger = logging.getLogger(__name__)


class NotificationService:
    SEND_SMS_ENDPOINT = "message/send"
    CONNECTION_TIMEOUT = 10

    @property
    def url(self):
        """The full URL for the SMS sending endpoint"""
        return f"{self.api_url}{self.SEND_SMS_ENDPOINT}"

    @property
    def headers(self):
        """The headers for the SMS sending endpoint's POST request"""
        api_token = self.api_token
        return {
            "Authorization": "Token " + api_token,
            "Content-Type": "application/json",
        }

    @staticmethod
    def data(sender, destinations, text):
        """The data/payload for the SMS sending endpoint's POST request"""
        return json.dumps(
            {
                "sender": sender,
                "to": [{"destination": d, "format": "mobile"} for d in destinations],
                "text": text,
            }
        )

    def __init__(self, api_token, api_url) -> None:
        self.api_token = api_token
        self.api_url = api_url
        super().__init__()

    def send_sms(self, sender, destinations, text):
        try:
            response = requests.post(
                url=self.url,
                data=self.data(sender, destinations, text),
                headers=self.headers,
                timeout=self.CONNECTION_TIMEOUT,
            )

            response.raise_for_status()
        except requests.exceptions.HTTPError:
            logger.exception("SMS message sent failed!")

        return response

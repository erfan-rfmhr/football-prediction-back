import json
import logging

import requests

from django.conf import settings


logger = logging.getLogger(__name__)


def _send_telegram_message(text: str) -> None:
    """Send a message to the configured admin chat via the Telegram Bot API."""
    bot_token = getattr(settings, "TELEGRAM_BOT_API_KEY", "")
    base_url = getattr(settings, "TELEGRAM_BASE_URL", "")
    chat_id = getattr(settings, "ADMIN_CHAT_ID", "")

    if not (bot_token and base_url and chat_id):
        logger.warning("Telegram credentials are not configured; skipping notification.")
        return

    url = f"{base_url.rstrip('/')}/bot{bot_token}/sendMessage"
    try:
        r = requests.post(
            url,
            data={"chat_id": chat_id, "text": text},
            timeout=5,
        )
    except requests.RequestException as exc:
        logger.exception("Failed to send Telegram error notification: %s", exc)


def _format_error_message(request, response) -> str:
    request_body = request.body.decode("utf-8", errors="replace")
    response_body = response.content.decode("utf-8", errors="replace")

    try:
        request_body = json.dumps(json.loads(request_body), indent=2)
    except (ValueError, TypeError):
        pass

    try:
        response_body = json.dumps(json.loads(response_body), indent=2)
    except (ValueError, TypeError):
        pass

    user = getattr(getattr(request, "user", None), "username", None) or "anonymous"

    return (
        f"Error {response.status_code} on {request.method} {request.get_full_path()}\n"
        f"User: {user}\n"
        f"Remote IP: {request.META.get('REMOTE_ADDR', '-')}\n"
        f"User-Agent: {request.META.get('HTTP_USER_AGENT', '-')}\n\n"
        f"Request payload:\n{request_body}\n\n"
        f"Response body:\n{response_body}"
    )


class ErrorResponseLoggingMiddleware:
    """Log HTTP error responses (4xx and 5xx) and notify the admin via Telegram."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if 400 <= response.status_code < 600:
            logger.error(
                "%s %s -> %s | request body: %s | response body: %s",
                request.method,
                request.get_full_path(),
                response.status_code,
                request.body.decode("utf-8", errors="replace"),
                response.content.decode("utf-8", errors="replace"),
            )
            try:
                _send_telegram_message(_format_error_message(request, response))
            except Exception as exc:
                logger.exception("Failed to send Telegram error notification: %s", exc)

        return response

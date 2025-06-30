"""
ARIN Waitlist Monitor v1.2

Monitor ARIN's IPV4 Waitlist for changes and reports
the current status of your waitlist entry in Slack.

Copyright (C) 2025 Winston Astrachan
Released under the terms of the MIT license
"""

import datetime
import json
import os
import time
from typing import Any, Dict, Optional

import requests

CACHE_KEY = "/run/arin-waitlist.last"


def _get_env_var(name: str, default: Any = None, required: bool = False) -> str:
    """Get the value of an environment variable with optional default and required validation.

    Args:
        name: The name of the environment variable to retrieve.
        default: The default value to return if the environment variable is not set.
                 Defaults to None.
        required: Whether the environment variable is required. If True and the
                  environment variable is not set, raises ValueError. Defaults to False.

    Returns:
        The value of the environment variable as a string, or the default value.

    Raises:
        ValueError: If the environment variable is not set and required is True.
    """
    try:
        return os.environ[name]
    except KeyError:
        if required:
            raise ValueError(
                f"The {name} environment variable is required but not set."
            )
        return default


def _get_cache_value(key: str) -> Optional[Any]:
    """Retrieve a cached value from the filesystem.

    Args:
        key: The cache key (file path) to read from.

    Returns:
        The cached value as a string, or None if the cache file doesn't exist.
    """
    try:
        with open(key) as f:
            return f.read().strip()
    except FileNotFoundError:
        return None


def _set_cache_value(key: str, value: Optional[Any]) -> Optional[Any]:
    """Store a value in the filesystem cache.

    Args:
        key: The cache key (file path) to write to.
        value: The value to store in the cache.

    Returns:
        The value that was stored.
    """
    with open(key, "w") as f:
        f.write(str(value))
    return value


def _get_headers() -> Dict[str, str]:
    """Build HTTP headers for Arin API requests.

    Returns:
        A dictionary containing the required HTTP headers for API requests.
    """
    return {
        "Accept": "application/json",
    }


def notify_slack(message: str) -> None:
    """Post a message to Slack via the Slack webhook

    Args:
        msg: The message to send to Slack
    """
    print(message)
    data = {
        "attachments": [
            {
                "color": "#F7852E",
                "pretext": "ARIN waitlist position has changed!",
                "fallback": message,
                "text": message,
            },
        ],
        "username": SLACK_TITLE,
        "icon_emoji": SLACK_EMOJI,
    }
    try:
        response = requests.post(
            SLACK_WEBHOOK_URL,
            data=json.dumps(data),
            headers={"Content-Type": "application/json"},
        )
        response.raise_for_status()
    except Exception as e:
        print(f"Failed to post to Slack: {e}")


def get_current_position() -> None:
    """Request current waitlist position from ARIN

    Fetches the current waitlist position from ARIN's waitlist API.
    If the position has changed, print the new position and post to Slack.
    """
    try:
        response = requests.get(ARIN_WAITLIST_URL, headers=_get_headers())
        response.raise_for_status()
    except Exception as e:
        print(f"Unable to load waitlist: {e}")
        return

    # Determine current position by searching for our waitlist time
    current_position = None
    last_position = _get_cache_value(CACHE_KEY)
    for entry_position, entry in enumerate(response.json()):
        entry_date = entry.get("waitListActionDate")
        if ARIN_WAITLIST_TIME == entry_date:
            current_position = entry_position
            break

    if not current_position and last_position and last_position != "None":
        notify_slack(
            "Waitlist entry no longer found!!! :champagne::champagne::champagne:"
        )
    elif last_position and str(current_position) != str(last_position):
        notify_slack(
            f"Current waitlist position: {current_position}\nPrevious position: {last_position}"
        )
    elif current_position:
        print(f"Current waitlist position: {current_position}")
    else:
        print("Waiting list entry not found.")

    # Update cache with new position
    _set_cache_value(CACHE_KEY, current_position)


if __name__ == "__main__":
    ARIN_WAITLIST_URL = _get_env_var(
        "ARIN_WAITLIST_URL", "https://accountws.arin.net/public/rest/waitingList"
    )
    ARIN_WAITLIST_TIME = _get_env_var("ARIN_WAITLIST_TIME", required=True)
    SLACK_WEBHOOK_URL = _get_env_var("SLACK_WEBHOOK_URL", required=True)
    SLACK_EMOJI = _get_env_var("SLACK_EMOJI", ":hourglass:")
    SLACK_TITLE = _get_env_var("SLACK_TITLE", "ARIN Waitlist Monitor")
    get_current_position()

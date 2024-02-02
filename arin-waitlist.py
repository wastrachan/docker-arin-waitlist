"""
ARIN Waitlist Monitor v1.1

Monitor ARIN's IPV4 Waitlist for changes and reports
the current status of your waitlist entry in Slack.

Copyright (C) 2024 Winston Astrachan
Released under the terms of the MIT license
"""

import datetime
import json
import os
import requests
import time


def _get_env_var(name, default=None):
    """Returns value of an environment variable, or a default value.

    Returns:
        - Value of environment variable if environment variable is set
        - Defaut value `default` if environment variable is not set

    Raises:
        ValueError if environment variable is not set AND `default` is False
    """
    try:
        return os.environ[name]
    except KeyError:
        if default is False:
            raise ValueError(
                "The {} environment variable is required but not set.".format(name)
            )
        return default


def _get_cache_value(key):
    """Returns a value for a cache key, or None"""
    address = None
    try:
        with open(key) as f:
            address = f.read()
    except FileNotFoundError:
        address = None
    return address


def _set_cache_value(key, value):
    """Sets or updates the value for a cache key"""
    with open(key, "w") as f:
        f.seek(0)
        f.write(str(value))
    return value


def _get_arin_headers():
    """Returns request headers for the ARIN API"""
    return {
        "Accept": "application/json",
    }


def notify(msg):
    """Call Slack webhook and post msg as a message"""
    print(msg)
    data = {
        "attachments": [
            {
                "color": "#F7852E",
                "pretext": "ARIN waitlist position has changed!",
                "fallback": msg,
                "text": msg,
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
        print("Failed to post to Slack: {}".format(e))


def get_current_position():
    """Request current waitlist position from ARIN"""
    try:
        response = requests.get(ARIN_WAITLIST_URL, headers=_get_arin_headers())
        response.raise_for_status()
    except Exception as e:
        print("Unable to load waitlist: {}".format(e))
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
        notify("Waitlist entry no longer found!!! :champagne::champagne::champagne:")
    elif last_position and str(current_position) != str(last_position):
        notify(
            "Current waitlist position: {}\nPrevious position: {}".format(
                current_position, last_position
            )
        )
    elif current_position:
        print("Current waitlist position: {}".format(current_position))
    else:
        print("Waiting list entry not found.")

    _set_cache_value(CACHE_KEY, current_position)


if __name__ == "__main__":
    CACHE_KEY = "/run/arin-waitlist.last"
    ARIN_WAITLIST_URL = _get_env_var(
        "ARIN_WAITLIST_URL", "https://accountws.arin.net/public/rest/waitingList"
    )
    ARIN_WAITLIST_TIME = _get_env_var("ARIN_WAITLIST_TIME", False)
    SLACK_WEBHOOK_URL = _get_env_var("SLACK_WEBHOOK_URL", False)
    SLACK_EMOJI = _get_env_var("SLACK_EMOJI", ":hourglass:")
    SLACK_TITLE = _get_env_var("SLACK_TITLE", "ARIN Waitlist Monitor")
    get_current_position()

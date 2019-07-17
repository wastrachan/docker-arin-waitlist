import re
import requests
import simplejson as json

from libs.environment import getenv


def info(message, webhook=None, emoji=None):
    """ Post a message at an info level to an alerts channel in Slack """
    post_message(message, color='#1F77D4', webhook=webhook, emoji=emoji)


def success(message, webhook=None, emoji=None):
    """ Post a message at a success level to an alerts channel in Slack """
    post_message(message, color='good', webhook=webhook, emoji=emoji)


def warning(message, webhook=None, emoji=None):
    """ Post a message at a warning level to an alerts channel in Slack """
    post_message(message, color='warning', webhook=webhook, emoji=emoji)


def error(message, webhook=None, emoji=None):
    """ Post a message at an error level to an alerts channel in Slack """
    post_message(message, color='danger', webhook=webhook, emoji=emoji)


def post_message(message, title=None, emoji=None, username=None, color=None, webhook=None):
    """ Post a message to an alerts channel an Slack

    Args:
        message (str): Message to post to channel
        title (str, optional): Optional message title
        emoji (str, optional): Emoji override to use for the message
        username (str, optional): Username override to user for the message
        color (str, optional): Color of the message, default of 'black'
            Can be one of 'good', 'warning', 'danger', or any hex color code
    """
    alert_color = '#000000'
    alert_emoji = getenv('SLACK_EMOJI', None)

    # Validate alert color
    if color:
        if color.lower() in ('good', 'warning', 'danger'):
            alert_color = color.lower()
        if re.match(r'#[\w\d]{3,6}', color.lower()):
            alert_color = color.upper()

    # Validate alert emoji
    if emoji:
        if re.match(r':[\w\d]+:]', emoji):
            alert_emoji = emoji

    data = {
        'attachments': [
            {
                'title': title if title else getenv('SLACK_TITLE', ''),
                'color': alert_color,
                'fallback': message,
                'text': message,
            },
        ],
    }

    # Replace emoji if provided
    if emoji:
        data['icon_emoji'] = alert_emoji

    # Replace username if provided
    if username:
        data['username'] = username

    # Use default webhook if one is not provided
    if webhook is None:
        webhook = getenv('SLACK_WEBHOOK_URL')

    # Post message to slack
    response = requests.post(webhook,
                             data=json.dumps(data),
                             headers={'Content-Type': 'application/json'})
    response.raise_for_status()

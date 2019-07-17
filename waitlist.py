import os
import time
import click
import requests
from requests.exceptions import HTTPError
from dotenv import load_dotenv

from libs.slack import info
from libs.environment import getenv


load_dotenv()
WAITLIST_URL = getenv('WAITLIST_URL', 'https://www.arin.net/rest/waitinglist')
WAITLIST_TIME = getenv('WAITLIST_TIME')


@click.command()
@click.option('--notify', default=False, is_flag=True, help='Send notification to Slack on any waitlist movement')
@click.option('--schedule', default=0, help='Schedule (in minutes) at which to re-run check')
def command(notify, schedule):
    """ Entrypoint for click command """
    if schedule:
        while True:
            waitlist(notify)
            print("Next check in {} minutes\n".format(schedule))
            time.sleep(schedule * 60)
    else:
        waitlist(notify)


def waitlist(notify):
    """ Request current waitlist position from ARIN

    Args:
        notify (bool) - Post notification to Slack on waitlist change, if true
    """
    print("Loading waitlist...")
    try:
        response = requests.get(WAITLIST_URL, headers={'accept': 'Application/JSON'})
        response.raise_for_status()
    except HTTPError as e:
        print("Unable to load waitlist: HTTP {} for URL {}".format(e, WAITLIST_URL))
        quit(1)

    data = response.json()
    current_position = None
    last_position = get_last_position()
    for entry in data.get('waitingListEntries', []):
        entry_date = entry.get('waitingListActionDate')
        entry_position = entry.get('index')
        if WAITLIST_TIME in entry_date:
            current_position = entry_position

    if not current_position:
        print("\nWaiting list entry not found! :champagne::champagne::champagne:")
        if notify:
            success("We weren't found on the waiting list! :champagne::champagne::champagne:")
        quit(0)
    print("\nCurrent waiting list position: {}".format(current_position))
    if last_position:
        if current_position != last_position:
            print("Last position was {}".format(last_position))
            if notify:
                info('Current waitlist position: {}\nPrevious Waitlist Position: {}'.format(current_position, last_position))
        else:
            print("No change from last postion.")

    set_last_position(current_position)


def get_last_position():
    """ Read the last position from a local cache file """
    cache_file = os.path.join(os.getcwd(), '.last_position')
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            try:
                return int(f.readlines()[0])
            except ValueError:
                pass
    return None


def set_last_position(position):
    """ Store the last position in a local cache file """
    cache_file = os.path.join(os.getcwd(), '.last_position')
    with open(cache_file, 'w+') as f:
        f.write("{}\r\n".format(position))


if __name__ == '__main__':
    command()

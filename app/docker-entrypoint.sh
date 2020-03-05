#!/usr/bin/env sh
set -e

# Check for required environment variables
if [[ -z "$ARIN_WAITLIST_TIME" ]]; then
    echo "The environment variable ARIN_WAITLIST_TIME is required, but was not set." 1>&2
    exit 1
fi
if [[ -z "$SLACK_WEBHOOK_URL" ]]; then
    echo "The environment variable SLACK_WEBHOOK_URL is required, but was not set." 1>&2
    exit 1
fi

# Generate CRON entry
echo "${UPDATE_SCHEDULE:-"*/5 * * * *"} python /arin-waitlist.py" > /etc/crontabs/root

# Exec CMD
exec "$@"

#!/usr/bin/env sh
set -e

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo " Starting arin-waitlist..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "    [+] Creating CRON entry..."
echo "${UPDATE_SCHEDULE:-"*/5 * * * *"} python /arin-waitlist.py" > /etc/crontabs/root

echo "    [+] Running..."
echo ""
exec "$@"

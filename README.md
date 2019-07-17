ARIN Waitlist Alert Tool
========================
This tool reads [ARIN's IPV4 Waitlist](https://www.arin.net/resources/guide/ipv4/waiting_list/) and reports the current status of _your_ waitlist entry in Slack.


## Disclaimer
This is one of those "I spent an hour after work" projects. I cobbled it together in an afternoon, and got it just to where it suited my needs. Feel free to use it as inspiration, fork it, hack it, whatever you need. It's by no means perfect.

## Configuration
This tool depends on a few environment variables. They can be provided in a `.env` file as follows:

| Variable | Description
|----------|------------
| WAITLIST_TIME | Required. Timestamp from your entry in ARIN's waitlist
| SLACK_WEBHOOK_URL | Required. Slack webhook URL
| SLACK_EMOJI | Optional. Specify an emoji to use for your webhook user
| SLACK_TITLE | Optional. Title for all Slack alerts

```
SLACK_EMOJI=":timhortons:"
SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR_WEBHOOk"
SLACK_TITLE="ARIN Waitlist"
WAITLIST_TIME="00:00:00 -0400"
```

## Running
This package includes a `Pipenv` file. Run `pipenv install` after cloning the project to set up dependencies.

`waitlist.py` supports several arguments:
```
Usage: waitlist.py [OPTIONS]

  Entrypoint for click command

Options:
  --notify            Send notification to Slack on any waitlist movement
  --schedule INTEGER  Schedule (in minutes) at which to re-run check
  --help              Show this message and exit.
```

## Docker
Examine the Dockerfile for configuration options when building the image. A Dockerfile was included that builds this project against pipenv docker images.

To build:

`docker build -t waitlist`

To run:

`docker run waitlist`


## License
The content of this project itself is licensed under the [MIT License](LICENSE).

# ARIN Waitlist Monitor

Monitor ARIN's IPV4 Waitlist for changes and reports the current status of your waitlist entry in Slack.

[![](https://circleci.com/gh/wastrachan/docker-arin-waitlist.svg?style=svg)](https://circleci.com/gh/wastrachan/docker-arin-waitlist)
[![](https://img.shields.io/docker/pulls/wastrachan/arin-waitlist.svg)](https://hub.docker.com/r/wastrachan/arin-waitlist)

## Install

#### Docker Hub

Pull the latest image from Docker Hub:

```shell
docker pull wastrachan/arin-waitlist
```

#### Manually

Clone this repository, and run `make build` to build an image:

```shell
git clone https://github.com/wastrachan/docker-arin-waitlist.git
cd docker-arin-waitlist
make build
```

If you need to rebuild the image, run `make clean build`.

## Run

#### Docker

Run this image manually with `docker run`. You'll need to define several environment variables for this container, and they are detailed below.

```shell
docker run --name arin-waitlist \
           -e ARIN_WAITLIST_TIME="Tue, 25 Feb 2020 13:07:29" \
           -e SLACK_WEBHOOK_URL="https://hooks.slack.com/services/TTtttttTT" \
           --restart unless-stopped \
           wastrachan/arin-waitlist:latest
```

## Configuration

Configuration is accomplished through the use of environment variables. The inclusive list is below.

#### Environment Variables

| Variable             | Required | Default                                 | Description                                                                                                                                                                                                                                                                                        |
| -------------------- | -------- | --------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `UPDATE_SCHEDULE`    | No       | `*/5 * * * *`                           | Cron-style schedule for waitlist updates.                                                                                                                                                                                                                                                          |
| `ARIN_WAITLIST_TIME` | Yes      | -                                       | The timestamp for your waitlist entry. You can locate this timestamp on the [IPV4 Waiting List](https://www.arin.net/resources/guide/ipv4/waiting_list/). The timestamp can be copied right off of this page-- but leave off the timezone. A valid entry may read `T2024-02-02T19:58:22.198+00:00` |
| `ARIN_WAITLIST_URL`  | No       | `https://www.arin.net/rest/waitinglist` | URL of the ARIN API.                                                                                                                                                                                                                                                                               |
| `SLACK_WEBHOOK_URL`  | Yes      | -                                       | [Webhook](https://slack.com/apps/A0F7XDUAZ-incoming-webhooks) URL created for your Slack workspace.                                                                                                                                                                                                |
| `SLACK_EMOJI`        | No       | `:hourglass:`                           | Customize the emoji displayed in your Slack alert.                                                                                                                                                                                                                                                 |
| `SLACK_TITLE`        | No       | `ARIN Waitlist Monitor`                 | Customize the name of your Slack alert.                                                                                                                                                                                                                                                            |

## License

The content of this project itself is licensed under the [MIT License](LICENSE).

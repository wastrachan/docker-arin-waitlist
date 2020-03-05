FROM python:3.8.1-alpine
LABEL maintainer="Winston Astrachan"
LABEL description="ARIN Waitlist Monitor"

COPY app/ /
RUN pip install -r /requirements.txt

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["crond", "-f", "-c", "/etc/crontabs/"]

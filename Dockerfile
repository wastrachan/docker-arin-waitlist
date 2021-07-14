FROM python:3.9.6-alpine
LABEL maintainer="Winston Astrachan"
LABEL description="ARIN Waitlist Monitor"

COPY app/ /
RUN pip install -r /requirements.txt

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["crond", "-f", "-c", "/etc/crontabs/"]

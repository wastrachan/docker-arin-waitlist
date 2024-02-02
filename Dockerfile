FROM python:3.12-alpine
LABEL org.opencontainers.image.title="ARIN Waitlist"
LABEL org.opencontainers.image.version="v1.1"
LABEL org.opencontainers.image.description="ARIN Waitlist Monitor"
LABEL org.opencontainers.image.source="https://github.com/wastrachan/docker-arin-waitlist"
LABEL org.opencontainers.image.authors="Winston Astrachan"
LABEL org.opencontainers.image.licenses="MIT"
ENV PYTHONUNBUFFERED=1 \
    LANG="C.UTF-8" \
    LANGUAGE="C.UTF-8" \
    LC_ALL="C.UTF-8" \
    LC_CTYPE="C.UTF-8"

COPY arin-waitlist.py /
COPY docker-entrypoint.py /
COPY requirements.txt /
RUN set -eux; \
    pip install -r /requirements.txt

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["crond", "-f", "-c", "/etc/crontabs/"]

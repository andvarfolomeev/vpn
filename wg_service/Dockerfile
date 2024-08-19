FROM python:3.12.5-alpine3.20


HEALTHCHECK CMD /usr/bin/timeout 5s /bin/sh -c "/usr/bin/wg show | /bin/grep -q interface || exit 1" --interval=1m --timeout=5s --retries=3

RUN apk add --no-cache \
    dpkg \
    dumb-init \
    iptables \
    iptables-legacy \
    wireguard-tools

RUN pip install --no-cache-dir poetry

WORKDIR /code/wg_wrapper
COPY wg_wrapper .

WORKDIR /code/wg_service
COPY wg_service/poetry.lock .
COPY wg_service/pyproject.toml .
RUN mkdir wg_service && touch wg_service/__init__.py

RUN poetry install --no-root --no-interaction
COPY wg_service .
RUN chmod +x ./start.sh

RUN update-alternatives --install /sbin/iptables iptables /sbin/iptables-legacy 10 --slave /sbin/iptables-restore iptables-restore /sbin/iptables-legacy-restore --slave /sbin/iptables-save iptables-save /sbin/iptables-legacy-save

EXPOSE 51871/udp
EXPOSE 8000/tcp

CMD ["./start.sh"]

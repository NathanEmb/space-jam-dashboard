FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

RUN apt-get -y update; apt-get -y install curl

WORKDIR /app

ADD . /app

ENV PATH="/app/.venv/bin:$PATH"

RUN uv sync --frozen 

CMD ["uv", "run", "panel", "serve", "src/frontend.py", "--address", "0.0.0.0", "--port", "5006", "--allow-websocket-origin=18.222.161.54:5006", "--liveness" ] 
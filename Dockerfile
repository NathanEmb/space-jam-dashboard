FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

WORKDIR /app

ADD . /app

ENV PATH="/app/.venv/bin:$PATH"

RUN uv sync --frozen 

CMD ["uv", "run", "panel", "serve", "src/frontend.py"]
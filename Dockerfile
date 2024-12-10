FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

RUN apt-get -y update; apt-get -y install curl

WORKDIR /app

ADD . /app

ENV PYTHONPATH=.

RUN uv sync --frozen 

CMD ["uv", "run",  "streamlit", "run", "src/frontend/Spacejam_Dashboard.py", "--server.port", "5006" ] 
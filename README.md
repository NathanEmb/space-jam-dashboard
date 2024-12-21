[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Deployment](https://github.com/NathanEmb/space-jam-dashboard/blob/main/.github/workflows/deploy.yaml/badge.svg)]
[![Better Stack Badge](https://uptime.betterstack.com/status-badges/v2/monitor/1pkz4.svg)](https://uptime.betterstack.com/?utm_source=status_badge)

# Space Jammers

Web dashboard for the Space Jam fantasy basketball league. It is currently hosted at https://space-jammers.com! The goal is tor 

## About
This project gets data from [espn-api](https://github.com/cwendt94/espn-api)  to create a basic web application using [Streamlit](https://streamlit.io/) as the web framework, Pandas for data manipulation, and [Jinja2](https://jinja.palletsprojects.com/en/stable/) for some html delivery inside the application.

## Contributing
### Bug Report or Feature Request
If you have requested features or bugs to report please use [GitHub Issues](https://github.com/NathanEmb/space-jam-dashboard)

### Code your own
This project uses [UV](https://github.com/astral-sh/uv) as the dependency manager and uses [Ruff](https://github.com/astral-sh/ruff) for linting and formatting. These rules are enforced on all Pull Requests. I recommend using a pre-commit hook or an IDE extension like [this](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff).
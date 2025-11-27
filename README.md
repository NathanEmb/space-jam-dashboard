# Space Jammers Dashboard

Web dashboard for the Space Jam fantasy basketball league. It is currently hosted at https://space-jammers.com!

## About

This project provides a dashboard for a fantasy basketball league (Space Jammers) that pulls data from ESPN's Fantasy API and displays various statistics and insights. The dashboard includes:

- Team statistics and category rankings
- Player performance metrics across different timeframes (7, 15, 30 days)
- Head-to-head matchup comparisons
- Trade analyzer to evaluate potential trades

## Architecture

The application is built using:

- [FastAPI](https://fastapi.tiangolo.com/) for the web backend and API
- [HTML + CSS](https://developer.mozilla.org/en-US/docs/Web) for the mobile-friendly frontend
- [ESPN API](https://github.com/cwendt94/espn-api) for fetching fantasy basketball data
- [Pandas](https://pandas.pydata.org/) for data manipulation and analysis
- [Jinja2](https://jinja.palletsprojects.com/) for HTML template rendering

The project is containerized with Docker and deployed to AWS.

## Project Structure

```
src/
├── app.py          # FastAPI application with routing and endpoints
├── backend.py      # Core logic for ESPN API data fetching and processing
├── constants.py    # League configuration and stat categories
└── frontend/
    ├── static/     # Static assets (CSS)
    │   └── css/
    │       └── base.css
    └── templates/  # Jinja2 HTML templates
        ├── base.html
        ├── index.html
        ├── matchup.html
        ├── team.html
        └── trade.html
```

## Features

- **Category Rankings**: Visualize team performance across 9 statistical categories
- **Team Viewer**: Detailed breakdown of individual team strengths, weaknesses, and trends
- **Matchup Viewer**: Compare head-to-head matchups with detailed statistics
- **Trade Analyzer**: Evaluate potential trades with projected stat impact analysis
- **Mobile-Friendly**: Optimized for mobile devices with responsive design and touch-friendly controls

## Development Setup

1. Ensure you have Python 3.12+ installed

2. Install dependencies using UV (recommended) or pip:
   ```bash
   uv sync
   # OR
   pip install -e .
   ```

3. Run the application locally:
   ```bash
   uv run uvicorn src.app:app --reload --port 5006
   # OR
   python -m uvicorn src.app:app --reload --port 5006
   ```

4. Open your browser and navigate to `http://localhost:5006`

## Deployment

The application is containerized using Docker:

```bash
docker build -t space-jammers .
docker run -p 5006:5006 space-jammers
```

Deployment to AWS is automated via GitHub Actions upon completion of a Pull Request to main.

## Contributing

1. Follow the existing code structure and style
2. Use appropriate docstrings for new functions
3. Test your changes locally before submitting PRs
4. Ensure mobile responsiveness for any UI changes

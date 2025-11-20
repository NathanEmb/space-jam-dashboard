# Space Jammers Dashboard

Web dashboard for the Space Jam fantasy basketball league. It is currently hosted at https://space-jammers.com!

## About

This project provides a dashboard for a fantasy basketball league (Space Jammers) that pulls data from ESPN's Fantasy API and displays various statistics and insights. The dashboard includes:

- Team statistics and category rankings
- Player performance metrics across different timeframes (7, 15, 30 days)
- Head-to-head matchup comparisons

## Architecture

The application is built using:

- [Streamlit](https://streamlit.io/) for the web frontend
- [ESPN API](https://github.com/cwendt94/espn-api) for fetching fantasy basketball data
- [Pandas](https://pandas.pydata.org/) for data manipulation and analysis
- [Matplotlib](https://matplotlib.org/) for data visualization
- [Jinja2](https://jinja.palletsprojects.com/) for HTML template rendering
- [Groq API](https://groq.com/) for generating AI content

The project is containerized with Docker and deployed to AWS.

## Project Structure

- `src/backend.py` - Core logic for data fetching and processing
- `src/prompts.py` - Prompting for AI-generated content via Groq
- `src/frontend/` - Streamlit pages and UI components
  - `Spacejam_Dashboard.py` - Main dashboard entry point
  - `figures.py` - Matplotlib visualization functions
  - `streamlit_utils.py` - Utility functions for Streamlit UI
  - `pages/` - Additional views (Team Viewer, Matchup Viewer)
  - `components/` - Reusable UI components with HTML templates

## Features

- **Category Rankings**: Visualize team performance across different statistical categories
- **Team Viewer**: Detailed breakdown of individual team strengths, weaknesses, and trends
- **Matchup Viewer**: Compare head-to-head matchups with detailed statistics
- **AI Commentary**: Enjoy witty, sometimes snarky comments about teams and matchups

## Development Setup

1. Ensure you have Python 3.13 installed

2. Install dependencies using UV (recommended) or pip:
   ```bash
   uv sync
   # OR
   pip install -e .
   ```

3. Run the application locally:
   ```bash
   uv run streamlit run src/frontend/Spacejam_Dashboard.py
   ```

## Deployment

The application is containerized using Docker:

```bash
docker build -t space-jammers .
docker run -p 5006:5006 space-jammers
```

Deployment to AWS is automated via GitHub Actions upon completion of a Pull Request to main.

## Environment Variables

- `GROQ_API_KEY` - Required for AI-generated content via the Groq API

## Contributing

1. Follow the existing code structure and style
2. Use appropriate docstrings for new functions
3. Test your changes locally before submitting PRs
# ReportGen — AI-Powered Business Report Generator

Upload any CSV or Excel file and get a professional PDF report with charts and AI-written insights in seconds.

🌐 **Live API:** [reports.webwatchhq.com/docs](https://reports.webwatchhq.com/docs)

## What it does

- Upload any CSV or Excel data file
- Automatically analyzes key metrics (min, max, mean, totals)
- Generates professional charts for every numeric column
- Claude AI writes a business narrative with insights and recommendations
- Downloads as a polished PDF report

## Tech Stack

- **Python + FastAPI** — REST API backend
- **Pandas** — data analysis and statistics
- **Matplotlib** — chart generation (bar charts per metric)
- **ReportLab** — PDF generation with embedded charts
- **Claude API (Anthropic)** — AI-written business narrative
- **Docker** — containerized deployment
- **AWS EC2** — 24/7 cloud deployment
- **Nginx + Let's Encrypt** — production web server with HTTPS
- **GitHub Actions** — CI/CD auto-deployment on push

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /upload | Upload and analyze a CSV or Excel file |
| POST | /generate-report | Generate AI report (JSON response) |
| POST | /download-report | Generate and download PDF report |

## How it works
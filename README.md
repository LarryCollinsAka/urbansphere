# UrbanSphere
A City that Listens, Learns and Understands, Speaks, Nurtures and Aids.

# Urban SDG Platform MVP

## Overview
A hackathon MVP for SDG 11: Sustainable Cities and Communities, built with Flask and a lightweight JavaScript frontend. Key features:
- Housing upgrade suggestions
- Urban air quality info
- Civic participation feedback

## Setup
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app/main.py
```

## Usage
- Open your browser at `http://localhost:5000`
- Try the buttons for Air Quality, Housing, and Civic Feedback

## Next Steps
- Integrate real APIs (Watsonx, WhatsApp, etc.)
- Connect to a database
- Expand endpoints and UI
---

## Folder Structure

```
project-root/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── housing.py
│   │   ├── air_quality.py
│   │   ├── civic.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── watsonx.py
│   │   ├── whatsapp.py
│   │   ├── air_quality.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── housing.py
│   │   ├── feedback.py
│   ├── db.py
│   ├── config.py
│   └── utils.py
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── main.js
│   └── images/
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── dashboard.html
│   ├── housing.html
│   ├── air_quality.html
│   ├── civic.html
├── tests/
│   ├── test_routes.py
│   ├── test_services.py
├── requirements.txt
├── .env
├── README.md
├── run.py
├── .github/
│   └── workflows/
│       └── ci-cd.yml

## Quick Start

1. **Clone the repo**
2. `python -m venv venv && source venv/bin/activate`
3. `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and fill in API keys
5. Run with `python src/app.py`
6. Set your webhook on WhatsApp Cloud API to `https://<your-render-url>/webhook`

---

## DevOps & MVC

- **MVC**: Models (data), Views (UI/templates), Controllers (logic)
- **DevOps**: GitHub Actions for simple CI/CD, auto-deploy to Render

---

## Contributing

1. Fork & clone
2. Make a new branch for your feature
3. Commit with clear messages
4. Make a Pull Request

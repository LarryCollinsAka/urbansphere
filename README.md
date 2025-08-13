# UrbanSphere
A City that Listens, Learns and Understands, Speaks, Nurtures and Aids.

# Sustainable Cities & Communities - SDG 11 Hackathon Project

## Project Overview
This project aims to empower citizens and city officials with tools for:
- Waste management and reporting
- Smart mobility solutions
- Urban safety and sustainability monitoring
- Community engagement
- All coordinated via WhatsApp and an admin dashboard

**Tech Stack**:  
- Python 3.x  
- Flask (MVC pattern)  
- WhatsApp Cloud API (Meta)  
- Render.com for deployment

---

## Folder Structure

```
project-root/
│
├── README.md
├── .gitignore
├── requirements.txt
├── .env.example
│
├── src/
│   ├── models/
│   ├── views/
│   ├── controllers/
│   ├── bot/
│   ├── static/
│   ├── templates/
│   ├── utils/
│   └── app.py
│
├── tests/
├── scripts/
├── .github/
│   └── workflows/
└── docs/
```

---

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

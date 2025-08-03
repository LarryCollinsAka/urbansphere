# UrbanSphere
A City that Listens, Learns and Understands, Speaks, Nurtures and Aids.

# 1. Clone project directory
git clone https://github.com/LarryCollinsAka/urbansphere.git
cd urbansphere

# 2. Create and activate a Python virtual environment
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# venv\Scripts\activate   # On Windows
UrbanSphere-Hackathon/
|-- venv/                  # Our virtual environment
|-- .env                   # Securely store API keys and secrets
|-- app.py                 # The main Flask application, Brenda's home
|-- agents/                # Directory for all our specialized agents
|   |-- __init__.py        # An empty file to make 'agents' a Python package
|   |-- sanita.py          # Sanita's logic and RAG knowledge base
|   |-- qumy.py            # Qumy's logic and RAG knowledge base
|   |-- nura.py            # Nura's logic and RAG knowledge base
|   |-- uby.py             # Uby's logic and RAG knowledge base
|   |-- zati.py            # Zati's logic and RAG knowledge base
|-- data/                  # Directory for our simulated JSON datasets
|   |-- sanita_data.json   # Simulated waste management data
|   |-- qumy_data.json     # Simulated public service data
|   |-- nura_data.json     # Simulated food security data
|   |-- uby_data.json      # Simulated urban planning data
|   |-- zati_data.json     # Simulated safety contacts data
|-- requirements.txt       # Lists all our project's Python dependencies

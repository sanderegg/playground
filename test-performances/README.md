# AIOHTTP Simple API

This is a simple AIOHTTP application with a single GET endpoint at the root path (`/`).

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

The server will start on http://0.0.0.0:8080

## API Endpoints

- `GET /`: Returns a JSON response with a "Hello, World!" message

# AIOHTTP Simple API

This is a simple AIOHTTP application with a single GET endpoint at the root path (`/`). It's optimized for performance using uvloop, orjson, and caching middleware.

## Setup Options

### Local Development

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

### Using Docker

This project includes Docker support for easy deployment and consistent environment across platforms.

#### Using the Makefile

```bash
# Build the Docker image
make build

# Run the container in detached mode
make run

# View all available commands
make help
```

#### Manual Docker Commands

```bash
# Build the Docker image
docker build -t aiohttp-server .

# Run the container
docker run -p 8080:8080 aiohttp-server
```

## API Endpoints

- `GET /`: Returns a JSON response with a "Hello, World!" message

## Performance Features

- **uvloop**: A fast drop-in replacement for asyncio's event loop
- **orjson**: High-performance JSON serialization/deserialization
- **caching**: Simple in-memory response caching for GET requests
- **optimized socket settings**: TCP_NODELAY and custom buffer sizes
- **worker optimization**: Automatically scales based on available CPU cores

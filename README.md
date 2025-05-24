# Embrapa Vitiviniculture API

A FastAPI application that serves data for the Embrapa Vitiviniculture research.

## Running with Docker

The easiest way to run this application is using Docker and Docker Compose.

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Setup

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd embrapa-vitiviniculture-api
   ```

2. Create a `.env` file from the example:
   ```bash
   cp .env.example .env
   ```
   
3. Build and start the containers:
   ```bash
   docker-compose up -d
   ```

4. The API will be available at: http://localhost:8000

5. To check the API documentation, visit: http://localhost:8000/docs

### Commands

- Start the application:
  ```bash
  docker-compose up -d
  ```

- View logs:
  ```bash
  docker-compose logs -f
  ```

- Stop the application:
  ```bash
  docker-compose down
  ```

- Rebuild the application after changes:
  ```bash
  docker-compose up -d --build
  ```

## Running locally

If you prefer to run the application without Docker:

1. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Create a `.env` file with your database connection:
   ```
   DATABASE_URL=sqlite:///local.db  # Or your preferred database URL
   ALLOW_REINGEST=false
   ```

3. Apply migrations:
   ```bash
   alembic upgrade head
   ```

4. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

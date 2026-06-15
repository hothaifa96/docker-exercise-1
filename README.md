# XO Game - Tic Tac Toe

A full-stack Tic Tac Toe game built with React, Flask, and PostgreSQL.

## Architecture

- **Frontend**: React 18 (port 3000)
- **Backend**: Python Flask (port 5000)
- **Database**: PostgreSQL 15 (port 5432)

## Quick Start with Docker

```bash
# Build and start all services
docker-compose up --build

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:5000
```

## Project Structure

```
.
├── backend/           # Flask API
│   ├── app.py        # Main application
│   ├── Dockerfile    # Backend container
│   └── requirements.txt
├── frontend/         # React app
│   ├── src/          # React source code
│   ├── public/       # Static assets
│   ├── Dockerfile    # Frontend container
│   └── nginx.conf    # Nginx configuration
├── database/         # Database scripts
│   └── init.sql      # Schema initialization
├── docker-compose.yml
└── .env.example      # Environment template
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/api/games` | Create new game |
| GET | `/api/games` | List all games |
| GET | `/api/games/<id>` | Get game by ID |
| POST | `/api/games/<id>/move` | Make a move (position: 0-8) |
| DELETE | `/api/games/<id>` | Delete game |

## Development Setup (without Docker)

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### Frontend
```bash
cd frontend
npm install
npm start
```

### Database
```bash
# Requires PostgreSQL running locally
createdb xogame
psql xogame < database/init.sql
```

## Environment Variables

Copy `.env.example` to `.env` and customize:

```env
DB_HOST=localhost
DB_NAME=xogame
DB_USER=postgres
DB_PASSWORD=postgres
DB_PORT=5432
REACT_APP_API_URL=http://localhost:5000
```

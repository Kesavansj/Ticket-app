# Ticket App — Flask REST API

## Project Structure

```
ticket-app/
├── app.py            # Main Flask app entry point
├── config.py         # DB config (reads from env vars)
├── db.py             # DB connection helper
├── auth_routes.py    # Register & Login endpoints
├── ticket_routes.py  # CRUD endpoints for tickets
├── ticket_model.py   # DB queries for tickets
├── init.sql          # Run this once to create DB tables
├── requirements.txt  # Python dependencies
└── .env.example      # Copy to .env and fill in your values
```

## Setup Instructions

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Set up environment variables
Copy `.env.example` to `.env` and fill in your Postgres credentials:
```bash
cp .env.example .env
```

### 3. Create the database tables
Connect to your Postgres DB and run:
```bash
psql -U postgres -d ticketdb -f init.sql
```

### 4. Run the app
```bash
python app.py
```

---

## API Endpoints

### Auth
| Method | Endpoint         | Description        |
|--------|------------------|--------------------|
| POST   | /auth/register   | Register a user    |
| POST   | /auth/login      | Login & get token  |

### Tickets (requires Bearer token)
| Method | Endpoint          | Description        |
|--------|-------------------|--------------------|
| POST   | /tickets/         | Create ticket      |
| GET    | /tickets/         | Get all tickets    |
| PUT    | /tickets/<id>     | Update a ticket    |
| DELETE | /tickets/<id>     | Delete a ticket    |

---

## Example Usage

### Register
```json
POST /auth/register
{ "username": "john", "password": "secret" }
```

### Login
```json
POST /auth/login
{ "username": "john", "password": "secret" }
```

### Create Ticket (add Authorization: Bearer <token> header)
```json
POST /tickets/
{ "name": "John", "task": "Fix bug", "description": "Login page crashes" }
```

# Study English With Tobi

An English listening and dictation training system with:

- FastAPI backend
- React frontend
- JWT authentication
- `edge-tts` audio generation
- PostgreSQL data storage
- Learning history and stats tracking
- Dictionary lookup with IPA and Vietnamese meanings
- Vocabulary and word lookup history

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Backend Stack](#backend-stack)
- [Frontend Stack](#frontend-stack)
- [Requirements](#requirements)
- [PostgreSQL Config](#postgresql-config)
- [PostgreSQL Setup](#postgresql-setup)
- [macOS](#macos)
- [Windows](#windows)
- [Verify Project Database](#verify-project-database)
- [Backend Setup](#backend-setup)
- [Frontend Setup](#frontend-setup)
- [Main API Endpoints](#main-api-endpoints)
- [Auth](#auth)
- [Training](#training)
- [History](#history)
- [Dictionary](#dictionary)
- [Example API Requests](#example-api-requests)
- [Register](#register)
- [Login](#login)
- [Practice](#practice)
- [Evaluate](#evaluate)
- [History Stats](#history-stats)
- [Dictionary Lookup](#dictionary-lookup)
- [Dictionary List](#dictionary-list)
- [Word Lookup History](#word-lookup-history)
- [Frequent Looked-up Words](#frequent-looked-up-words)
- [Learning Flow](#learning-flow)
- [Notes](#notes)
- [Future Improvements](#future-improvements)
- [License](#license)

## Features

- Register and login with JWT authentication
- Generate TTS audio with `en-US-AriaNeural`
- Practice sentence-by-sentence dictation
- Play audio in normal, slow, and 1.25x speed
- Evaluate user input with word-level diff feedback
- Track learning history per user
- Show learning stats and accuracy trend
- Click words to open dictionary popup
- Cache dictionary results in SQLite
- Track user word lookup history
- Search and paginate dictionary entries
- Play pronunciation audio for each dictionary word

## Project Structure

```text
tts-learn-listening/
├── app/
│   ├── auth/
│   ├── dictionary/
│   ├── history/
│   ├── routes/
│   ├── main.py
│   ├── database.py
│   ├── evaluator.py
│   ├── tts.py
│   └── voice_results/
├── frontend/
│   ├── src/
│   ├── package.json
│   └── vite.config.js
├── .env
├── requirements.txt
└── README.md
```

## Backend Stack

- FastAPI
- PostgreSQL
- `psycopg`
- JWT with `python-jose`
- Password hashing with `bcrypt`
- `edge-tts`
- SQLite cache for dictionary data

## Frontend Stack

- React
- Vite
- React Router
- Simple custom CSS

## Requirements

- Python 3.11+ recommended
- Node.js 18+ recommended
- PostgreSQL running locally

## PostgreSQL Config

This project loads database config from `.env`.

Recommended config:

- Database: `ttsdb`
- User: `ttsuser`
- Password: `root`
- Host: `localhost`
- Port: `5432`

You can override them with environment variables:

```bash
export POSTGRES_HOST=localhost
export POSTGRES_PORT=5432
export POSTGRES_DB=ttsdb
export POSTGRES_USER=ttsuser
export POSTGRES_PASSWORD=root
export JWT_SECRET_KEY=your-secret-key
```

Example backend `.env`:

```env
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=ttsdb
POSTGRES_USER=ttsuser
POSTGRES_PASSWORD=root
JWT_SECRET_KEY=change-this-in-production
```

## PostgreSQL Setup

This project expects a PostgreSQL database with:

- Database: `ttsdb`
- User: `ttsuser`
- Password: `root`

### macOS

Install PostgreSQL with Homebrew:

```bash
brew install postgresql
brew services start postgresql
```

Open PostgreSQL shell:

```bash
psql postgres
```

Create database user and database:

```sql
CREATE USER ttsuser WITH PASSWORD 'root';
CREATE DATABASE ttsdb OWNER ttsuser;
GRANT ALL PRIVILEGES ON DATABASE ttsdb TO ttsuser;
```

Exit:

```sql
\q
```

Test connection:

```bash
psql -h localhost -U ttsuser -d ttsdb
```

### Windows

Download and install PostgreSQL:

- [https://www.postgresql.org/download/windows/](https://www.postgresql.org/download/windows/)

During installation:

- remember the `postgres` superuser password
- keep the default port `5432` unless you want a custom one

Open:

- SQL Shell (`psql`)

Then connect using the default `postgres` superuser and run:

```sql
CREATE USER ttsuser WITH PASSWORD 'root';
CREATE DATABASE ttsdb OWNER ttsuser;
GRANT ALL PRIVILEGES ON DATABASE ttsdb TO ttsuser;
```

Exit:

```sql
\q
```

Test connection:

```bash
psql -h localhost -U ttsuser -d ttsdb
```

### Verify Project Database

If the connection works, the app will automatically create its tables on startup.

Run backend:

```bash
uvicorn app.main:app --reload
```

Then check the tables:

```bash
psql -h localhost -U ttsuser -d ttsdb
```

Inside `psql`:

```sql
\dt
```

You should see tables like:

- `users`
- `learning_history`
- `user_word_history`

## Backend Setup

```bash
cd tts-learn-listening
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Run backend:

```bash
source venv/bin/activate
uvicorn app.main:app --reload
```

Notes:

- backend auto-loads `.env`
- dictionary cache is stored in `dictionary_cache.db`
- generated audio is stored in `app/voice_results`

Backend will run at:

```text
http://127.0.0.1:8000
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

## Frontend Setup

```bash
cd tts-learn-listening/frontend
npm install
npm run dev
```

Frontend will run at:

```text
http://localhost:5173
```

If needed, configure backend URL in:

- `frontend/.env`

Example:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

## Main API Endpoints

### Auth

- `POST /auth/register`
- `POST /auth/login`
- `GET /auth/me`

### Training

- `POST /tts`
- `POST /practice`
- `POST /evaluate`
- `GET /tts/word?word=example`

### History

- `GET /history`
- `GET /history/stats`

### Dictionary

- `GET /dictionary?word=example`
- `GET /dictionary/list?page=1&limit=10&search=example`
- `GET /dictionary/words/history`
- `GET /dictionary/words/frequent`

## Example API Requests

### Register

```bash
curl -X POST http://127.0.0.1:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"alice@example.com","password":"111111"}'
```

### Login

```bash
curl -X POST http://127.0.0.1:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"alice@example.com","password":"111111"}'
```

### Practice

```bash
curl -X POST http://127.0.0.1:8000/practice \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"sentence":"Hello world."}'
```

### Evaluate

```bash
curl -X POST http://127.0.0.1:8000/evaluate \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"sentence":"Hello world.","user_input":"Hello word."}'
```

### History

```bash
curl http://127.0.0.1:8000/history \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### History Stats

```bash
curl http://127.0.0.1:8000/history/stats \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Dictionary Lookup

```bash
curl "http://127.0.0.1:8000/dictionary?word=example" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Dictionary List

```bash
curl "http://127.0.0.1:8000/dictionary/list?page=1&limit=10&search=example" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Word Lookup History

```bash
curl "http://127.0.0.1:8000/dictionary/words/history" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Frequent Looked-up Words

```bash
curl "http://127.0.0.1:8000/dictionary/words/frequent" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Learning Flow

1. User registers or logs in
2. User pastes a paragraph into the frontend
3. Frontend splits it into sentences
4. Backend generates practice audio
5. User types what they hear
6. Backend evaluates the answer
7. Result is stored in learning history
8. User clicks words to open dictionary details
9. Dictionary results are cached locally
10. User reviews progress on the history and vocabulary pages

## Notes

- Generated audio files are stored in:
  - `app/voice_results`
- Audio is served from:
  - `/static/audio/...`
- Learning history is stored per authenticated user
- `/history` and `/history/stats` only return current user data
- dictionary cache is stored in:
  - `dictionary_cache.db`
- `/dictionary/words/history` and `/dictionary/words/frequent` only return current user data
- frontend includes:
  - login/register
  - practice screen
  - learning history screen
  - vocabulary screen

## Future Improvements

- Refresh tokens
- Password reset flow
- Admin roles
- Richer analytics charts
- Lesson management
- Content library upload

## License

This project is licensed under the MIT License.

See [LICENSE](/LICENSE) for details.

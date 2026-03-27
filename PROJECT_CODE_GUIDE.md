# Code Analysis for Beginners

This document helps you read and learn the project from the perspective of someone new to Python, FastAPI, React, and how frontend communicates with backend.

## 1. What does this project do?

This is an English listening learning system.

The FastAPI backend will:
- Generate audio files from text using `edge-tts`
- Create pronunciation audio for each word in dictionary popup
- Grade dictation using `difflib`
- Manage login with JWT
- Save learning history to PostgreSQL
- Store dictionary in SQLite cache

The React frontend will:
- Allow users to input paragraphs
- Split into individual sentences
- Call backend to generate audio
- Let users type what they heard
- Show grading results
- Look up words, view learning history and vocabulary

If you learn this project well, you will learn:
- Basic Python and backend code organization
- FastAPI routes, services, auth, database
- React state, effects, router, auth context
- How frontend and backend communicate through APIs

## 2. Overall Architecture

The project is split into 2 parts:

### Backend

Directory: [app](tts-learn-listening/app)

Main components:
- [main.py](tts-learn-listening/app/main.py): FastAPI startup point
- [tts.py](tts-learn-listening/app/tts.py): create mp3 files
- [evaluator.py](tts-learn-listening/app/evaluator.py): grade dictation
- [database.py](tts-learn-listening/app/database.py): connect to PostgreSQL and create tables
- [auth/](tts-learn-listening/app/auth): register, login, JWT
- [routes/training.py](tts-learn-listening/app/routes/training.py): `/tts`, `/practice`, `/evaluate`
- [history/](tts-learn-listening/app/history): learning history
- [dictionary/](tts-learn-listening/app/dictionary): word lookup, cache, lookup history

### Frontend

Directory: [frontend/src](tts-learn-listening/frontend/src)

Main components:
- [main.jsx](tts-learn-listening/frontend/src/main.jsx): React app mount point
- [App.jsx](tts-learn-listening/frontend/src/App.jsx): app-wide routing
- [lib/api.js](tts-learn-listening/frontend/src/lib/api.js): API call functions
- [auth/AuthContext.jsx](tts-learn-listening/frontend/src/auth/AuthContext.jsx): manage token and user
- [pages/PracticePage.jsx](tts-learn-listening/frontend/src/pages/PracticePage.jsx): main learning screen
- [pages/HistoryPage.jsx](tts-learn-listening/frontend/src/pages/HistoryPage.jsx): learning history
- [pages/VocabularyPage.jsx](tts-learn-listening/frontend/src/pages/VocabularyPage.jsx): vocabulary and dictionary search
- [components/DictionaryModal.jsx](tts-learn-listening/frontend/src/components/DictionaryModal.jsx): word meaning popup
- [components/Word.jsx](tts-learn-listening/frontend/src/components/Word.jsx): render individual clickable words

## 3. What order should you read in?

If you're new to this, here's a very reasonable reading order:

1. [README.md](tts-learn-listening/README.md)
2. [app/main.py](tts-learn-listening/app/main.py)
3. [app/routes/training.py](tts-learn-listening/app/routes/training.py)
4. [app/tts.py](tts-learn-listening/app/tts.py)
5. [app/evaluator.py](tts-learn-listening/app/evaluator.py)
6. [app/auth/utils.py](tts-learn-listening/app/auth/utils.py)
7. [app/database.py](tts-learn-listening/app/database.py)
8. [app/dictionary/service.py](tts-learn-listening/app/dictionary/service.py)
9. [frontend/src/App.jsx](tts-learn-listening/frontend/src/App.jsx)
10. [frontend/src/auth/AuthContext.jsx](tts-learn-listening/frontend/src/auth/AuthContext.jsx)
11. [frontend/src/lib/api.js](tts-learn-listening/frontend/src/lib/api.js)
12. [frontend/src/pages/PracticePage.jsx](tts-learn-listening/frontend/src/pages/PracticePage.jsx)
13. [frontend/src/pages/VocabularyPage.jsx](tts-learn-listening/frontend/src/pages/VocabularyPage.jsx)

Reasoning:
- You'll see the main data flows first
- Then dive into auth, database and dictionary
- On the frontend side, also read from general routing to specific pages

## 4. Backend FastAPI: Learning Python through this project

### 4.1. Backend Entry Point

File: [app/main.py](tts-learn-listening/app/main.py)

This is the first file you should read in the backend.

It shows you:
- How the FastAPI app is created
- CORS middleware so frontend can call APIs
- Where static files are mounted
- How routers are included in the app

You'll see:
- `init_db()` to create PostgreSQL tables
- `init_dictionary_cache()` to create SQLite cache for dictionary
- `app.mount("/static/audio", ...)` to serve mp3 files

Python/FastAPI concepts you'll learn:
- Application creation function
- Module imports
- Splitting routers into multiple files
- Resource initialization at startup

### 4.2. Training Routes

File: [app/routes/training.py](tts-learn-listening/app/routes/training.py)

This is the heart of the listening learning app.

It has 4 main endpoints:
- `POST /tts`
- `POST /practice`
- `POST /evaluate`
- `GET /tts/word`

You'll learn:
- `pydantic` models to validate input
- `async def` for asynchronous tasks
- `Depends(get_current_user)` to require login
- Calling service functions instead of embedding all logic in routes

For example:
- `/practice` receives a sentence
- Calls `generate_audio_file(...)` twice for normal and slow speed
- Returns 2 audio URLs

This is a very good backend design pattern for beginners:
- Route receives request
- Service handles business logic
- Route returns response

### 4.3. TTS Service

File: [app/tts.py](tts-learn-listening/app/tts.py)

This file is very easy to learn Python from because it's concise but practical.

It teaches you:
- `Enum` in Python
- `Path` for working with file paths
- `async/await`
- Calling external library `edge_tts`

Some nice points:
- `SpeechSpeed` only allows `normal` and `slow`
- `RATE_BY_SPEED` is a dictionary mapping speed to TTS rate
- `generate_audio_file()` generates filename using `uuid4`
- `generate_word_audio_file()` saves files by normalized word name to avoid regeneration

From this file you can learn:
- How to write clear, meaningful code
- How to separate constants from business logic
- How to save generated files in a dedicated directory

### 4.4. Dictation Grading

File: [app/evaluator.py](tts-learn-listening/app/evaluator.py)

If you're new to Python, this file is very worth reading carefully.

It uses:
- `re` to tokenize
- `difflib.SequenceMatcher` to compare 2 sentences

It returns:
- `accuracy`
- `diff`
- `correct_sentence`

From here you'll learn:
- lists
- dictionaries
- `for` loops
- `if/elif` conditions
- How to turn a "string comparison" problem into data for frontend display

Note that:
- Backend doesn't return HTML
- Backend returns JSON with clear structure
- Frontend will use the `type` of `diff` to colorize and display errors

### 4.5. Authentication

Files:
- [app/auth/routes.py](tts-learn-listening/app/auth/routes.py)
- [app/auth/utils.py](tts-learn-listening/app/auth/utils.py)

This section teaches you many practical backend concepts:
- Hash passwords with `bcrypt`
- Create JWT
- Read JWT to get current user
- OAuth2PasswordBearer in FastAPI

A very important detail:
- Passwords should not be stored in plaintext
- Code hashes password first before saving to DB
- Every request requiring auth goes through `get_current_user`

Important concepts:
- `create_access_token(...)`: create token
- `authenticate_user(...)`: verify email/password
- `get_current_user(...)`: verify token and get user

If you want to learn backend properly, try to draw the flow:

1. Frontend calls `/auth/login`
2. Backend verifies password
3. Backend returns JWT
4. Frontend stores token
5. Frontend sends token in `Authorization` header
6. Backend reads token in protected routes

### 4.6. Database PostgreSQL

File: [app/database.py](tts-learn-listening/app/database.py)

This file shows you how backend connects to real database.

It uses:
- `psycopg`
- `.env`
- `load_dotenv(...)`

You'll learn:
- Reading environment variables
- Creating database connections
- Running raw SQL
- `fetchone()`, `fetchall()`
- Helper functions to read/write data

Main tables:
- `users`
- `learning_history`
- `user_word_history`

This is a good project to learn step by step:
- You don't need SQLAlchemy yet
- SQL is clearly visible
- Easy to understand what each table is used for

### 4.7. Dictionary Service

Files:
- [app/dictionary/routes.py](tts-learn-listening/app/dictionary/routes.py)
- [app/dictionary/service.py](tts-learn-listening/app/dictionary/service.py)

This is the module with the most knowledge.

It teaches you:
- Calling external APIs with `httpx`
- Normalizing data
- Caching in SQLite
- Retry/fallback when API fails
- Translation from English to Vietnamese
- Saving user lookup history

This section uses 2 databases:
- PostgreSQL: store user data and user history
- SQLite: store dictionary cache for faster lookup

Very good backend ideas:
- `normalize_word(word)` to avoid duplicates
- `get_word(word)` reads cache first
- `save_word(data)` uses upsert to avoid saving duplicates
- `translate_to_vi(text)` separated into its own function

This is an extremely valuable lesson:
- Good code doesn't just "work"
- Good code must also consider caching, duplicates, fallback and performance

### 4.8. History Module

Files:
- [app/history/routes.py](tts-learn-listening/app/history/routes.py)
- [app/history/service.py](tts-learn-listening/app/history/service.py)

This is where you learn how to separate business logic.

Similar to dictionary:
- Route only handles HTTP
- Service handles data processing

You'll learn how to:
- Save learning results every time `/evaluate` is called
- Get the 50 most recent records
- Calculate statistics like `average_accuracy`

## 5. Frontend React: Learning React through this project

### 5.1. App and Routes

File: [frontend/src/App.jsx](tts-learn-listening/frontend/src/App.jsx)

This file teaches you:
- React Router
- Public routes and protected routes

You'll see:
- `/login`
- `/register`
- `/`
- `/history`
- `/vocabulary`

If you're new to React, remember:
- React doesn't automatically "have pages"
- React uses router to map URLs to components

### 5.2. Auth Context

File: [frontend/src/auth/AuthContext.jsx](tts-learn-listening/frontend/src/auth/AuthContext.jsx)

This is a very important file for learning basic state management.

It manages:
- token
- user
- login
- register
- logout
- Check session when app first opens

You'll learn:
- `createContext`
- `useContext`
- `useEffect`
- `useMemo`
- Sharing logic across multiple pages

Note the flow:
- App opens
- `useEffect` calls `/auth/me`
- If token is valid, get user
- If token is broken, delete token

This is a very practical pattern for apps with auth.

### 5.3. Common API Layer

File: [frontend/src/lib/api.js](tts-learn-listening/frontend/src/lib/api.js)

This file is small but very important.

It helps:
- Store token in `localStorage`
- Automatically attach `Authorization: Bearer ...`
- Centralize `fetch` logic in one place

From here you learn a very valuable frontend lesson:
- Don't write `fetch(...)` scattered in every file
- Should have 1 common API layer

### 5.4. Practice Page

File: [frontend/src/pages/PracticePage.jsx](tts-learn-listening/frontend/src/pages/PracticePage.jsx)

This is the largest file and also the file that helps you learn React fastest.

You'll see:
- `useState` for many different states
- `useMemo` to calculate `currentSentence` and `currentWords`
- `useRef` to manage audio and dictionary cache
- Many async functions calling backend

Main lessons:

#### Split paragraph into sentences

Function `splitIntoSentences(paragraph)` teaches you:
- Regex in JavaScript
- Text input processing

#### Call practice API

Function `requestPractice(sentence)` teaches you:
- How to call backend
- Error handling with `try/catch`
- Handle `401`
- Update state after receiving response

#### Call evaluate API

Function `handleEvaluate()` teaches you:
- Send user data to server
- Receive JSON results
- Save to state to re-render UI

#### Play audio

Function `playAudio(speed, rate = 1)` teaches you:
- Create `Audio` object with JavaScript
- Change `playbackRate`
- Use `useRef` to keep audio object between renders

#### Dictionary popup

Function `handleWordClick(word)` teaches you:
- Frontend caching with `Map`
- Avoid calling API again for the same word
- Open modal with returned data

In [DictionaryModal.jsx](tts-learn-listening/frontend/src/components/DictionaryModal.jsx), you'll learn more:
- How to add a functional button to popup
- How to call `GET /tts/word?word=...`
- How to create `Audio` object and play word pronunciation

If you read this file carefully, you'll learn:
- What is state
- What are event handlers
- How components render based on state
- Why React apps must clearly separate state

### 5.5. Vocabulary Page

File: [frontend/src/pages/VocabularyPage.jsx](tts-learn-listening/frontend/src/pages/VocabularyPage.jsx)

This is an extremely useful file to learn:
- Search
- Debounce
- Pagination
- Keyword highlighting

You'll see:
- `searchInput`
- `debouncedSearch`
- `page`
- `pagination`

Flow:
- User types in search
- `useEffect` waits 300ms
- Then updates `debouncedSearch`
- Another `useEffect` calls `/dictionary/list`

This is a very practical frontend lesson:
- Don't call API every time user presses a key
- Debounce helps optimize requests

### 5.6. Modal and Small Components

Files:
- [frontend/src/components/DictionaryModal.jsx](tts-learn-listening/frontend/src/components/DictionaryModal.jsx)
- [frontend/src/components/Word.jsx](tts-learn-listening/frontend/src/components/Word.jsx)
- [frontend/src/components/ProtectedRoute.jsx](tts-learn-listening/frontend/src/components/ProtectedRoute.jsx)

This is a lesson about componentization.

Remember:
- Small components are easy to read
- Easy to test
- Easy to reuse

For example:
- `ProtectedRoute` contains route protection logic
- `Word` contains logic for displaying a clickable word
- `DictionaryModal` contains popup display logic

## 6. Data Flow in the System

Imagine a user's learning session:

1. User logs in on frontend
2. Frontend stores JWT in `localStorage`
3. User inputs paragraph
4. Frontend splits into individual sentences
5. Frontend calls `POST /practice`
6. Backend creates 2 audio files
7. Frontend plays audio
8. User types what they heard
9. Frontend calls `POST /evaluate`
10. Backend grades and saves `learning_history`
11. Frontend shows accuracy and diff
12. User clicks a word
13. Frontend calls `GET /dictionary?word=...`
14. Backend checks SQLite cache
15. If not found, calls dictionary API + translation API
16. Backend saves cache and saves `user_word_history`
17. Frontend shows modal with word meaning

If you want to learn fullstack properly, read code following this flow.

## 7. What You Learn About Python?

From this project, you can learn Python in layers:

### Basic Level

- Variables, functions, `if`, `for`
- `dict`, `list`, `str`
- Import modules
- Split code into files

### Intermediate Level

- `async def` and `await`
- `Enum`
- `Path`
- Regex
- `try/except`
- Type hints like `dict[str, Any]`

### Real Backend Level

- FastAPI
- Pydantic models
- JWT
- bcrypt
- PostgreSQL
- SQLite cache
- Call external APIs with `httpx`

## 8. What You Learn About React?

### Basic Level

- Function components
- JSX
- Props
- Event handlers

### Intermediate Level

- `useState`
- `useEffect`
- `useMemo`
- `useRef`
- React Router

### Real App Level

- Auth context
- Protected routes
- API layer
- Loading state
- Empty state
- Modal
- Search debounce
- Pagination

## 9. How to Read Code for Easy Understanding

Here are good ways to read code for beginners:

### Method 1: Read from top to bottom

For example with [app/routes/training.py](tts-learn-listening/app/routes/training.py):
- Read request model first
- Read route
- See what service the route calls
- Open that service and read more

### Method 2: Follow one feature

For example dictionary feature:
- Frontend clicks word in [PracticePage.jsx](tts-learn-listening/frontend/src/pages/PracticePage.jsx)
- Calls [api.js](tts-learn-listening/frontend/src/lib/api.js)
- Backend receives at [routes.py](tts-learn-listening/app/dictionary/routes.py)
- Processes at [service.py](tts-learn-listening/app/dictionary/service.py)
- Returns JSON to frontend
- Frontend renders at [DictionaryModal.jsx](tts-learn-listening/frontend/src/components/DictionaryModal.jsx)

### Method 3: Add temporary logs

If you don't understand how code runs, add:

```python
print("payload:", payload)
print("result:", result)
```

or in React:

```js
console.log("practiceData", practiceData);
```

This is a very practical learning method.

## 10. Self-Learning Exercises Perfect for This Project

If you want to learn fast, try these small exercises yourself:

### Exercise 1

Add new audio speed:
- `very_slow = "-40%"`

You'll modify:
- [app/tts.py](tts-learn-listening/app/tts.py)
- [frontend/src/pages/PracticePage.jsx](tts-learn-listening/frontend/src/pages/PracticePage.jsx)

### Exercise 2

Add `/profile` endpoint

You'll learn:
- Auth
- New route
- Return JSON user

### Exercise 3

Add high/low accuracy filter in learning history

You'll modify:
- Backend history route
- Frontend history page

### Exercise 4

Add "Save favorite word" button

You'll learn:
- Add database table
- Add route
- Add frontend button

### Exercise 5

Show number of wrong words in evaluate results

You'll modify:
- [app/evaluator.py](tts-learn-listening/app/evaluator.py)
- [frontend/src/pages/PracticePage.jsx](tts-learn-listening/frontend/src/pages/PracticePage.jsx)

## 11. Lessons About Code Design

This project also teaches you how to organize code cleanly:

### Separate Routes and Services

Don't let routes do too much work.

Good approach:
- Route receives request
- Service handles logic
- Database helper handles save/read data

### Separate Auth into Its Own Module

Auth is complex, so separating it makes maintenance easier.

### Cache Dictionary

Don't always call external APIs.

This is an important lesson:
- Reduce requests
- Faster
- More stable

### Frontend Has Separate API Layer

Don't scatter token and fetch across every page.

## 12. Important Keywords You Should Remember

- `async`: runs asynchronously
- `await`: waits for result of async function
- `JWT`: user authentication token
- `bcrypt`: hash passwords
- `route`: API path
- `service`: contains business logic
- `state`: changing data in React
- `effect`: logic that runs when component mounts or when dependency changes
- `cache`: temporarily store results for faster reuse
- `upsert`: if exists then update, if not exists then insert

## 13. 7-Day Learning Suggestion

### Day 1

Read:
- [README.md](tts-learn-listening/README.md)
- [app/main.py](tts-learn-listening/app/main.py)
- [frontend/src/App.jsx](tts-learn-listening/frontend/src/App.jsx)

Goal:
- Understand app overview

### Day 2

Read:
- [app/tts.py](tts-learn-listening/app/tts.py)
- [app/routes/training.py](tts-learn-listening/app/routes/training.py)

Goal:
- Understand request/response and audio flow

### Day 3

Read:
- [app/evaluator.py](tts-learn-listening/app/evaluator.py)
- [frontend/src/pages/PracticePage.jsx](tts-learn-listening/frontend/src/pages/PracticePage.jsx)

Goal:
- Understand dictation and evaluation

### Day 4

Read:
- [app/auth/utils.py](tts-learn-listening/app/auth/utils.py)
- [frontend/src/auth/AuthContext.jsx](tts-learn-listening/frontend/src/auth/AuthContext.jsx)

Goal:
- Understand fullstack auth

### Day 5

Read:
- [app/database.py](tts-learn-listening/app/database.py)
- [app/history/service.py](tts-learn-listening/app/history/service.py)

Goal:
- Understand DB and saving history

### Day 6

Read:
- [app/dictionary/service.py](tts-learn-listening/app/dictionary/service.py)
- [frontend/src/pages/VocabularyPage.jsx](tts-learn-listening/frontend/src/pages/VocabularyPage.jsx)

Goal:
- Understand external APIs, cache, search, pagination

### Day 7

Implement 1 small feature yourself.

For example:
- Add a new button
- Add a new field to DB
- Add a new endpoint

This is the day that helps you transition from "reading code" to "writing code".

## 14. Conclusion

This project is very suitable for learning fullstack because it has everything:
- Real backend
- Real frontend
- Auth
- Database
- External APIs
- Audio
- Dictionary
- History

If you're a beginner, don't try to read everything in 1 day.

Choose 1 specific flow, for example:
- Login
- Practice
- Evaluate
- Dictionary

Then follow the request from frontend to backend and back again.

That's the fastest way to learn.

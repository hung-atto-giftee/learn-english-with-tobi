# Codebase Guide For Beginners

This document is for people who are new to:

- Python
- FastAPI
- React
- Fullstack application structure

The goal is to help you understand this project step by step, and use it as a learning resource.

## What This Project Does

This project is an English listening trainer.

Users can:

- register and log in
- paste a paragraph
- practice dictation sentence by sentence
- listen to generated audio
- evaluate what they typed
- look up word meanings and IPA
- review learning history
- review vocabulary history

So this is a good real-world project to learn:

- backend APIs
- authentication
- database access
- frontend state management
- API integration
- fullstack data flow

## High-Level Architecture

There are 2 main parts:

1. Backend: FastAPI
2. Frontend: React + Vite

The backend is responsible for:

- authentication
- generating TTS audio
- evaluating dictation
- storing user history
- dictionary lookup
- database operations

The frontend is responsible for:

- rendering UI
- handling user input
- calling backend APIs
- showing loading, errors, and results

## Folder Structure

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
│   │   ├── auth/
│   │   ├── components/
│   │   ├── lib/
│   │   └── pages/
│   └── package.json
├── README.md
├── CODEBASE_GUIDE.md
└── requirements.txt
```

## Part 1: Backend Overview

The backend lives inside [`app/`](/Users/hungatto/Desktop/tts-learn-listening/app).

Main files:

- [`main.py`](/Users/hungatto/Desktop/tts-learn-listening/app/main.py)
- [`database.py`](/Users/hungatto/Desktop/tts-learn-listening/app/database.py)
- [`tts.py`](/Users/hungatto/Desktop/tts-learn-listening/app/tts.py)
- [`evaluator.py`](/Users/hungatto/Desktop/tts-learn-listening/app/evaluator.py)

Feature folders:

- [`auth/`](/Users/hungatto/Desktop/tts-learn-listening/app/auth)
- [`history/`](/Users/hungatto/Desktop/tts-learn-listening/app/history)
- [`dictionary/`](/Users/hungatto/Desktop/tts-learn-listening/app/dictionary)

### `main.py`

[`main.py`](/Users/hungatto/Desktop/tts-learn-listening/app/main.py) is the application entry point.

It:

- creates the FastAPI app
- enables CORS
- mounts static audio files
- initializes databases
- registers routers

This is usually the first backend file to read.

### `database.py`

[`database.py`](/Users/hungatto/Desktop/tts-learn-listening/app/database.py) manages PostgreSQL connection and table creation.

Important concepts here:

- environment variables
- DB connection creation
- schema initialization
- helper functions for database access

When learning backend, notice how DB logic is separated from route logic.

That separation is important because:

- routes stay clean
- database code is reusable
- easier to test and maintain

### `tts.py`

[`tts.py`](/Users/hungatto/Desktop/tts-learn-listening/app/tts.py) handles text-to-speech generation using `edge-tts`.

It:

- chooses the voice
- creates audio files
- stores them in `app/voice_results`

This file is a good example of isolating one responsibility into one module.

### `evaluator.py`

[`evaluator.py`](/Users/hungatto/Desktop/tts-learn-listening/app/evaluator.py) compares:

- original sentence
- user input

It uses word-level diff logic to calculate:

- accuracy
- missing words
- wrong words

This is a good file to study if you want to learn:

- text processing
- Python list/string handling
- business logic separated from HTTP routes

## Part 2: Backend Feature Modules

### Authentication

Files:

- [`auth/routes.py`](/Users/hungatto/Desktop/tts-learn-listening/app/auth/routes.py)
- [`auth/models.py`](/Users/hungatto/Desktop/tts-learn-listening/app/auth/models.py)
- [`auth/utils.py`](/Users/hungatto/Desktop/tts-learn-listening/app/auth/utils.py)

This module teaches:

- request/response models
- password hashing
- JWT tokens
- current user dependency

Important idea:

The backend uses dependency injection with FastAPI.

Example:

- `Depends(get_current_user)`

This means:

- before entering the route
- FastAPI will run `get_current_user`
- if token is invalid, request is rejected

That is a very important FastAPI pattern.

### History

Files:

- [`history/routes.py`](/Users/hungatto/Desktop/tts-learn-listening/app/history/routes.py)
- [`history/models.py`](/Users/hungatto/Desktop/tts-learn-listening/app/history/models.py)
- [`history/service.py`](/Users/hungatto/Desktop/tts-learn-listening/app/history/service.py)

This module teaches:

- service layer pattern
- response schemas
- separating statistics logic from route logic

The route should be thin.

The service should do the main work.

That is a strong backend design habit.

### Dictionary

Files:

- [`dictionary/routes.py`](/Users/hungatto/Desktop/tts-learn-listening/app/dictionary/routes.py)
- [`dictionary/service.py`](/Users/hungatto/Desktop/tts-learn-listening/app/dictionary/service.py)

This module teaches:

- external API calls
- fallback strategies
- normalization
- local caching
- migration/cleanup logic

It is a very practical module because it contains:

- normalization of words
- cache lookup first
- external fetch second
- save to cache
- user lookup history tracking

That pattern appears a lot in production systems.

## Part 3: Backend Request Flow

Here is one simple example flow for dictionary lookup:

1. Frontend calls `GET /dictionary?word=example`
2. Route validates and normalizes the word
3. Service checks SQLite cache
4. If cached:
   returns cached result
5. If not cached:
   calls external dictionary API
6. Service translates English meaning to Vietnamese
7. Service saves result to cache
8. Service records user word lookup history
9. Result returns to frontend

This is a great flow to study because it combines:

- auth
- route handling
- service logic
- cache
- database
- external API

## Part 4: Frontend Overview

The frontend lives in [`frontend/src/`](/Users/hungatto/Desktop/tts-learn-listening/frontend/src).

Main areas:

- [`App.jsx`](/Users/hungatto/Desktop/tts-learn-listening/frontend/src/App.jsx)
- [`auth/`](/Users/hungatto/Desktop/tts-learn-listening/frontend/src/auth)
- [`components/`](/Users/hungatto/Desktop/tts-learn-listening/frontend/src/components)
- [`pages/`](/Users/hungatto/Desktop/tts-learn-listening/frontend/src/pages)
- [`lib/api.js`](/Users/hungatto/Desktop/tts-learn-listening/frontend/src/lib/api.js)

### `App.jsx`

[`App.jsx`](/Users/hungatto/Desktop/tts-learn-listening/frontend/src/App.jsx) defines routes.

It shows how React Router is used to navigate between:

- login
- register
- practice
- learning history
- vocabulary

### `lib/api.js`

[`lib/api.js`](/Users/hungatto/Desktop/tts-learn-listening/frontend/src/lib/api.js) is the frontend API helper.

It:

- stores token in localStorage
- attaches `Authorization: Bearer ...`
- centralizes API calls

This is an important frontend pattern:

instead of repeating fetch logic everywhere, centralize it.

### Auth Context

[`auth/AuthContext.jsx`](/Users/hungatto/Desktop/tts-learn-listening/frontend/src/auth/AuthContext.jsx) is used for shared authentication state.

This teaches:

- React Context
- shared user state
- login/logout functions
- restoring session from localStorage

If you are new to React, this is a very good file to study slowly.

### Pages

Pages are full screens:

- [`pages/AuthPage.jsx`](/Users/hungatto/Desktop/tts-learn-listening/frontend/src/pages/AuthPage.jsx)
- [`pages/PracticePage.jsx`](/Users/hungatto/Desktop/tts-learn-listening/frontend/src/pages/PracticePage.jsx)
- [`pages/HistoryPage.jsx`](/Users/hungatto/Desktop/tts-learn-listening/frontend/src/pages/HistoryPage.jsx)
- [`pages/VocabularyPage.jsx`](/Users/hungatto/Desktop/tts-learn-listening/frontend/src/pages/VocabularyPage.jsx)

Study them in this order:

1. `AuthPage.jsx`
2. `PracticePage.jsx`
3. `HistoryPage.jsx`
4. `VocabularyPage.jsx`

That order goes from simpler to more advanced.

### Components

Components are reusable UI pieces:

- [`components/ProtectedRoute.jsx`](/Users/hungatto/Desktop/tts-learn-listening/frontend/src/components/ProtectedRoute.jsx)
- [`components/Word.jsx`](/Users/hungatto/Desktop/tts-learn-listening/frontend/src/components/Word.jsx)
- [`components/DictionaryModal.jsx`](/Users/hungatto/Desktop/tts-learn-listening/frontend/src/components/DictionaryModal.jsx)

These files teach:

- component reuse
- passing props
- keeping page components cleaner

## Part 5: Frontend Request Flow

Example: user clicks a word in the sentence.

1. `PracticePage.jsx` renders clickable word chips
2. user clicks a word
3. frontend checks local cache in memory
4. if not cached, frontend calls `/dictionary?word=...`
5. backend returns IPA and meanings
6. frontend opens `DictionaryModal`

This teaches:

- event handling
- async requests in React
- state updates
- modal rendering

## Part 6: Python Concepts You Can Learn Here

This project is good for learning these Python topics:

- functions
- modules
- imports
- dictionaries and lists
- string processing
- JSON serialization
- async / await
- exception handling
- database access
- API request handling
- project structure

### Example Patterns to Notice

#### 1. Pure function style

Files like [`evaluator.py`](/Users/hungatto/Desktop/tts-learn-listening/app/evaluator.py) contain logic that does not depend on HTTP.

That makes the code:

- easier to test
- easier to reuse

#### 2. Async I/O

FastAPI routes and dictionary/TTS functions use `async`.

Use `async` when the work is mostly:

- network
- file I/O
- waiting on external services

#### 3. Separation of concerns

Try to notice:

- routes handle HTTP
- services handle business logic
- database helpers handle persistence

That is one of the biggest lessons in backend engineering.

## Part 7: React Concepts You Can Learn Here

This project is good for learning:

- `useState`
- `useEffect`
- `useMemo`
- `useRef`
- React Router
- Context API
- controlled inputs
- loading state handling
- conditional rendering
- reusable components

### Example Patterns to Notice

#### 1. Controlled input

Search boxes and text inputs use:

- `value={state}`
- `onChange={...}`

This is the standard React way.

#### 2. Derived state with `useMemo`

Pages use `useMemo` for computed values like:

- current sentence
- filtered or grouped display values

#### 3. Debounced search

`VocabularyPage.jsx` uses delayed search updates.

This is useful because:

- fewer API requests
- smoother UX

## Part 8: Good Files To Read First

If you are totally new, use this reading order:

### Backend order

1. [`app/main.py`](/Users/hungatto/Desktop/tts-learn-listening/app/main.py)
2. [`app/routes/training.py`](/Users/hungatto/Desktop/tts-learn-listening/app/routes/training.py)
3. [`app/evaluator.py`](/Users/hungatto/Desktop/tts-learn-listening/app/evaluator.py)
4. [`app/tts.py`](/Users/hungatto/Desktop/tts-learn-listening/app/tts.py)
5. [`app/auth/utils.py`](/Users/hungatto/Desktop/tts-learn-listening/app/auth/utils.py)
6. [`app/history/service.py`](/Users/hungatto/Desktop/tts-learn-listening/app/history/service.py)
7. [`app/dictionary/service.py`](/Users/hungatto/Desktop/tts-learn-listening/app/dictionary/service.py)

### Frontend order

1. [`frontend/src/App.jsx`](/Users/hungatto/Desktop/tts-learn-listening/frontend/src/App.jsx)
2. [`frontend/src/lib/api.js`](/Users/hungatto/Desktop/tts-learn-listening/frontend/src/lib/api.js)
3. [`frontend/src/auth/AuthContext.jsx`](/Users/hungatto/Desktop/tts-learn-listening/frontend/src/auth/AuthContext.jsx)
4. [`frontend/src/pages/AuthPage.jsx`](/Users/hungatto/Desktop/tts-learn-listening/frontend/src/pages/AuthPage.jsx)
5. [`frontend/src/pages/PracticePage.jsx`](/Users/hungatto/Desktop/tts-learn-listening/frontend/src/pages/PracticePage.jsx)
6. [`frontend/src/components/DictionaryModal.jsx`](/Users/hungatto/Desktop/tts-learn-listening/frontend/src/components/DictionaryModal.jsx)
7. [`frontend/src/pages/HistoryPage.jsx`](/Users/hungatto/Desktop/tts-learn-listening/frontend/src/pages/HistoryPage.jsx)
8. [`frontend/src/pages/VocabularyPage.jsx`](/Users/hungatto/Desktop/tts-learn-listening/frontend/src/pages/VocabularyPage.jsx)

## Part 9: Suggested Exercises For Learning

Here are good beginner exercises you can do in this repo.

### Python / backend exercises

1. Add a new field to history response.
2. Add a new route that returns the latest practiced sentence.
3. Add a new dictionary fallback word to the mock map.
4. Add logging to one API route.
5. Add a limit parameter to `/dictionary/words/history`.

### React / frontend exercises

1. Add a clear button to the vocabulary search box.
2. Add a copy word button inside the dictionary modal.
3. Show a badge for cached dictionary results.
4. Add a filter for high accuracy history only.
5. Add a favorite words section.

## Part 10: How To Learn From This Project

A good way to learn is:

1. Run the app.
2. Use one feature.
3. Trace which frontend file handles it.
4. Trace which backend route is called.
5. Trace which service/database helper runs next.
6. Make one tiny change.
7. Run again.

That cycle is much better than trying to read the entire codebase at once.

## Part 11: Beginner Mindset Tips

- Do not try to understand everything in one pass.
- Follow one feature end to end.
- Read code with the app open and running.
- Make tiny edits and observe what changes.
- Use logs and print statements when confused.
- Prefer understanding flow over memorizing syntax.

## Summary

This project is a very good learning codebase because it includes:

- backend APIs
- auth
- database
- caching
- external API integration
- React pages
- modals
- state management
- fullstack request flow

If you study this repo feature by feature, you can learn both Python and React in a practical way.


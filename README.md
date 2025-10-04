# SQLBot Project

SQLBot is a simple chat bot that logs conversations to a database and responds to
user messages using a language‑model back‑end.  It also ships with a command
line interface, a small analysis tool, a REST API built with FastAPI and a
configurable database layer that can run on SQLite or Postgres via
environment variables.  Basic unit tests and a GitHub Actions workflow are
provided out of the box.

## Features

* **Chat Client** – Send messages from the command line or via HTTP and
  capture responses in a persistent database.
* **LLM Integration** – Use OpenAI’s API (or any compatible API) by
  specifying an API key in your `.env` file.  A stub function is used
  automatically if no key is provided.
* **Database Abstraction** – Use SQLite by default or point to a Postgres
  instance via the `DATABASE_URL` environment variable (for example
  `postgresql://user:password@localhost/sqlbot`).  SQLAlchemy handles the
  connection under the hood.
* **FastAPI Server** – Start a web server with `/chat` and `/conversations`
  endpoints to integrate SQLBot into other applications.
* **Safety Guard** – Simple SQL injection guard to prevent destructive
  statements from being executed.
* **Test Suite** – Basic unit tests using `pytest` to cover the guard and
  database functions.
* **Continuous Integration** – A GitHub Actions workflow runs the test
  suite on every push.

## Getting Started

### 1. Clone the repository and install dependencies

```bash
git clone <your‑fork‑here>
cd sqlbot
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure your environment

Copy the provided `.env.example` to `.env` and fill in any sensitive values:

```bash
cp .env.example .env
# Then edit .env to set DATABASE_URL or OPENAI_API_KEY if desired
```

If you do not specify a `DATABASE_URL` the application will fall back to
SQLite (`sqlite:///conversations.db`).  If you leave `OPENAI_API_KEY`
unset the bot will echo your input rather than call a remote model.

### 3. Initialize the database

Run the setup script once to create the tables:

```bash
python db_setup.py
```

### 4. Use the chat client

You can run a single message directly from the command line:

```bash
python bot_client.py --user "alice" --message "Hello, SQLBot!"
```

Alternatively, omit the flags to enter an interactive REPL where you can
type messages one after the other.  Quit the REPL by pressing Ctrl+C.

### 5. Run the FastAPI server

To expose your bot over HTTP, launch the server with Uvicorn:

```bash
uvicorn api:app --reload --port 8000
```

Then POST a JSON payload to `/chat` like so:

```bash
curl -X POST http://localhost:8000/chat -H "Content-Type: application/json" \
  -d '{"user":"alice","message":"Hello via HTTP"}'
```

You can also list previous conversations via GET `/conversations`.

### 6. Run the analysis tool

The `analysis.py` script prints a summary of conversations stored in the
database:

```bash
python analysis.py
```

### 7. Running tests

Install `pytest` (already included in `requirements.txt`) and run:

```bash
pytest
```

## Environment Variables

The following variables can be configured in your `.env` file:

| Variable         | Purpose                                                   |
|------------------|-----------------------------------------------------------|
| `DATABASE_URL`   | SQLAlchemy DB URL, e.g. `sqlite:///conversations.db`       |
| `OPENAI_API_KEY` | API key for OpenAI chat completion API (optional)         |
| `MODEL_NAME`     | Optional model name to use with the OpenAI API           |

## Contributing

Feel free to extend SQLBot with new features!  Pull requests are welcome.

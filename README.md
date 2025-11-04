# 🍫 BrownieGate — Flask Login Example

This repository is a minimal, opinionated example showing how to integrate Flask-Login with the BrownieGate Python package (BrownieGate). It demonstrates typical authentication flows, session handling, and two small example apps that illustrate cookie-based and non-cookie-based integrations.

This example is intended for learning and prototyping only. It shows:
- how to authenticate users using the BrownieGate SDK
- how to adapt BrownieGate user objects for Flask-Login
- how to persist sessions either with BrownieGate-encrypted cookies or with server-side sessions
- a simple, clean UI to exercise the flows

Python package: https://github.com/Bwownie/BrownieGate-package
BrownieGate docs: https://www.browniegate.xyz/dev/docs

---

## 🚀 Quick overview

- with_cookies/: example that uses encrypted cookies provided/validated via BrownieGate
- without_cookies/: example that uses a short server-side session tied to BrownieGate-authenticated identity
- templates/: shared templates used by the examples
- static/: CSS used by the example UI
- run.py: convenience entrypoint to run either example
- requirements.txt: Python dependencies (includes BrownieGate as a dependency)

---

## 🧰 Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/Bwownie/BrownieGate-flask-login-example.git
cd BrownieGate-flask-login-example
```

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate    # macOS / Linux
.venv\Scripts\activate       # Windows (PowerShell)
```

Install runtime dependencies:

```bash
pip install -r requirements.txt
```

For local development of the BrownieGate package (edit & test the SDK locally), install the package in editable mode from your local clone:

```bash
# from the sibling directory where you cloned the package
pip install -e ../BrownieGate-package
```

Or install the latest package directly from the repo:

```bash
pip install -U git+https://github.com/Bwownie/BrownieGate-package
```

---

## ⚙️ Configuration (.env)

Create a .env file at the repository root (do NOT commit secrets). The example apps expect these environment variables. The names below match the current example project's .env (PROJECT_UUID, API_KEY, ENCRYPTION_KEY). Make sure the variables you set match exactly those referenced in your code.

Example .env (replace placeholders):

PROJECT_UUID=''     # Enter your project UUID provided by BrownieGate
API_KEY=''          # Enter your API key provided by BrownieGate
ENCRYPTION_KEY=''   # Enter your Fernet encryption key provided by BrownieGate

# Flask / local settings
SECRET_KEY='replace-with-a-secure-random-string'
FLASK_ENV=development
FLASK_APP=run.py

Notes:
- The examples in this repo currently read PROJECT_UUID, API_KEY, and ENCRYPTION_KEY from the environment (these names match the included .env file you provided).
- SECRET_KEY must be set before creating the Flask app (sessions and CSRF depend on it).
- If you change environment variable names in the code, update .env accordingly. Alternatively, update the code to use BROWNIEGATE_* style variables if you prefer namespacing.

---

## ▶️ Running the examples

There are two example directories to illustrate different session strategies. From the repository root:

Run the cookie-based example:

```bash
# run.py accepts an environment variable to select example; default is with_cookies
export EXAMPLE=with_cookies
export FLASK_APP=run.py
export FLASK_ENV=development
flask run
# or
python run.py --example with_cookies
```

Run the non-cookie (server-side session) example:

```bash
export EXAMPLE=without_cookies
python run.py --example without_cookies
```

Open http://127.0.0.1:5000/ in your browser.

 Endpoints:
- /login — sign in
- /logout — sign out
- /home — protected page (requires login)

The "with_cookies" example demonstrates how BrownieGate-provided encrypted cookies can keep a user logged in across browser restarts (when configured). The "without_cookies" example shows a simple server-side session lifecycle.

---

## How BrownieGate integrates (high-level)

- The Flask app calls functions from the BrownieGate client (for example, to authenticate users or verify cookies).
- The returned BrownieGate user object is adapted to Flask-Login by a small adapter (implements get_id(), is_active, etc.). The adapter code lives in the app package used by the examples.
- Flask-Login handles session management on top of that adapter. For cookie flows the app relies on BrownieGate to produce/validate encrypted cookie payloads.

---

## Project structure

- run.py — lightweight entrypoint used to select / run an example
- with_cookies/ — Flask app demonstrating BrownieGate cookie integration
- without_cookies/ — Flask app demonstrating server-side session integration
- templates/ — shared Jinja2 templates (base.html, login.html, home.html)
- static/ — CSS and small assets
- requirements.txt — pinned dependencies

---

## Security notes (important)

This repo is for demonstration. Do not use it in production without hardening:
- Always use HTTPS (TLS) in production.
- Use a secure SECRET_KEY and never commit it.
- Ensure the BrownieGate encryption key and API key are kept secret.
- Review cookie flags (Secure, HttpOnly, SameSite) and session expiry to match your security posture.

---

## License & author

Author: Bwownie  
BrownieGate package: https://github.com/Bwownie/BrownieGate-package

See LICENSE in this repository for license details.

Acknowledgements: built as a small demonstration of integrating Flask-Login with the BrownieGate Python SDK.

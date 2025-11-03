# BrownieGate — Flask Login Example

A minimal example application demonstrating user authentication and session management in Flask using Flask-Login and BrownieGate. This repository is intended as a learning/reference project showing how to:

- log in and log out
- protect views with login_required
- use Flask-Login's user loader and session handling
- structure a small Flask app with basic templates and configuration

This project is intentionally small and easy to read so you can copy and adapt patterns into your own apps.

Contents
- templates/: Jinja2 templates for pages (login, home)
- requirements.txt: Python dependencies
- run.py: development entrypoint

Requirements
- Python
- pip

Installation (local dev)
1. Clone the repository
   git clone https://github.com/Bwownie/BrownieGate-flask-login-example.git
   cd BrownieGate-flask-login-example
   cd with_cookies OR without_cookies

3. Create and activate a virtual environment
   python -m venv .venv
   source .venv/bin/activate   # macOS / Linux
   .venv\Scripts\activate      # Windows (PowerShell)

4. Install dependencies
   pip install -r requirements.txt

Configuration
The app uses environment variables for configuration. For local development create a .env file.

Variables:
- PROJECT_UUID = your project uuid from BrownieGate
- API_KEY = your api key from BrownieGate
- ENCRYPTION_KEY = your encyrption key from BrownieGate

Running the app
Start the Flask development server:

python run.py

The app will be available at http://localhost:5000/ or http://your-ip:5000/

Usage
- Visit /login to sign in.
- Visit protected view page /home
- Use the logout button to end the session.
- With cookie example you can close the browser and reopen and remain logged in.

Security notes (important)
This repo is an instructional example. Before using any code here in production:
- Use HTTPS (TLS) in production.
- Implement rate-limiting, CSRF protection on forms (Flask-WTF), and session hardening.

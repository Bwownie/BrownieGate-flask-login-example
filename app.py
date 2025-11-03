from flask import Flask, render_template, url_for, redirect, request
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
from browniegate import BrownieClient
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

PROJECT_UUID = os.getenv('PROJECT_UUID', '')
API_KEY = os.getenv('API_KEY', '')
ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY', '')
BROWNIE_GATE_URL = 'https://www.browniegate.xyz'
brownie_gate_url = f'{BROWNIE_GATE_URL}/gate/auth?project_uuid={PROJECT_UUID}'

app = Flask(__name__)
app.secret_key = os.urandom(24)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

brownieclient = BrownieClient(
    api_key=API_KEY,
    project_uuid=PROJECT_UUID,
    encryption_key=ENCRYPTION_KEY,
    debug=True
)

class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# --- Routes ---
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login')
def login():
    print("BrownieGate URL:", brownie_gate_url)
    return render_template('login.html', brownie_gate_url=brownie_gate_url)

@app.route('/home')
@login_required
def home():
    return render_template('home.html', user_id=current_user.id)

@app.route('/callback')
def callback():
    payload = request.args.get("payload")
    if not payload:
        return "Missing payload", 400

    try:
        decrypted = brownieclient.decrypt_payload(payload)
        success, user_id = brownieclient.verify_payload(decrypted)
    except Exception:
        return "Invalid payload or verification error", 400

    if not success:
        return "Authentication failed", 401

    user = User(user_id)
    login_user(user)

    return redirect(url_for("home"))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
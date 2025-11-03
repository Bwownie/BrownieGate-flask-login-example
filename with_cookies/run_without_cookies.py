from flask import Flask, render_template, url_for, redirect, request, make_response, session
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
from browniegate import BrownieClient
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

PROJECT_UUID = os.getenv('PROJECT_UUID', '')
API_KEY = os.getenv('API_KEY', '')
ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY', '')
BROWNIE_GATE_URL = 'https://www.browniegate.xyz'
COOKIE_SAMESITE = os.getenv('COOKIE_SAMESITE')
brownie_gate_url = f'{BROWNIE_GATE_URL}/gate/auth?project_uuid={PROJECT_UUID}'

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config.update(SESSION_COOKIE_HTTPONLY=True)

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
    def __init__(self, user_id, username=None):
        self.id = user_id
        self.username = username


@app.before_request
def load_user_from_cookie():
    if current_user.is_authenticated or request.endpoint == 'static':
        return

    token = request.cookies.get('auth')
    if not token:
        return

    try:
        user_id, cookie_hash = brownieclient.decrypt_cookie(token)
        success = brownieclient.validate_cookie(user_id, cookie_hash)
    except Exception:
        success = False
        user_id = None

    if success and user_id:
        success, data = brownieclient.get_user_data(user_id)
        session['username'] = data.get("username") if success else None
        user = User(user_id, session.get('username'))
        login_user(user)
    else:
        resp = make_response(redirect(url_for('login')))
        resp.delete_cookie('auth')
        return resp


@login_manager.user_loader
def load_user(user_id):
    username = session.get('username')
    return User(user_id, username)


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login')
def login():
    return render_template('login.html', brownie_gate_url=brownie_gate_url)


@app.route('/home')
@login_required
def home():
    return render_template('home.html', username=current_user.username)


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

    token = brownieclient.generate_cookie(user_id)
    token_str = token.decode() if isinstance(token, bytes) else str(token)

    success, data = brownieclient.get_user_data(user_id)
    username = data.get("username") if success else None
    session['username'] = username 

    resp = make_response(redirect(url_for('home')))
    resp.set_cookie('auth', token_str, max_age=60*60*24*7)

    user = User(user_id, username)
    login_user(user)

    return resp


@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('username', None)
    resp = make_response(redirect(url_for('login')))
    resp.delete_cookie('auth')
    return resp

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
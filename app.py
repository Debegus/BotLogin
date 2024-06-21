from flask import Flask, redirect, url_for, session, request
import msal
from config import CLIENT_ID, CLIENT_SECRET, AUTHORITY, REDIRECT_PATH, SCOPE, SECRET_KEY, TELEGRAM_BOT_URL
import os

app = Flask(__name__)
app.secret_key = SECRET_KEY

@app.route('/')
def index():
    return "Bienvenido a la página de autenticación. Use /login para iniciar sesión."

@app.route('/login')
def login():
    session["flow"] = _build_auth_code_flow()
    return redirect(session["flow"]["auth_uri"])

@app.route('/authorized')
def authorized():
    try:
        cache = _load_cache()
        result = _build_msal_app(cache=cache).acquire_token_by_auth_code_flow(session.get("flow", {}), request.args)
        if "error" in result:
            return f"Login failure: {result['error']}"
        session["user"] = result.get("id_token_claims")
        _save_cache(cache)
        # Redirigir de vuelta al bot de Telegram con el token de sesión
        chat_id = session.get("chat_id")
        if chat_id:
            return redirect(f"{TELEGRAM_BOT_URL}/authenticated?session_id={session['user']['oid']}&chat_id={chat_id}")
        return "Login exitoso, pero falta chat_id"
    except ValueError:
        pass
    return redirect(url_for("index"))

@app.route('/set_chat_id')
def set_chat_id():
    chat_id = request.args.get('chat_id')
    session['chat_id'] = chat_id
    return "Chat ID seteado"

def _build_auth_code_flow():
    return _build_msal_app().initiate_auth_code_flow(SCOPE, redirect_uri=url_for("authorized", _external=True))

def _build_msal_app(cache=None):
    return msal.ConfidentialClientApplication(
        CLIENT_ID, authority=AUTHORITY,
        client_credential=CLIENT_SECRET, token_cache=cache)

def _load_cache():
    cache = msal.SerializableTokenCache()
    if session.get("token_cache"):
        cache.deserialize(session["token_cache"])
    return cache

def _save_cache(cache):
    if cache.has_state_changed:
        session["token_cache"] = cache.serialize()

if __name__ == "__main__":
    app.run(debug=True)

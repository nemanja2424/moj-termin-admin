from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token
from werkzeug.middleware.proxy_fix import ProxyFix
import os
from dotenv import load_dotenv

# Učitavanje .env fajla
load_dotenv()

# Kreiranje Flask aplikacije
app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET")  # nemanjica
jwt = JWTManager(app)

# ProxyFix omogućava Flask-u da vidi ispravne rute iza reverse proxy-ja
# x_prefix=1 znači da koristi prvi segment URL-a (/api) kao SCRIPT_NAME
app.wsgi_app = ProxyFix(app.wsgi_app, x_prefix=1)

# Test ruta
@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify({"message": "Zdravo iz Flask API-ja!"})

# Ruta za login koja vraća token koji ne ističe
@app.route('/api/token', methods=['POST'])
def get_token():
    data = request.json
    if data.get("username") == os.getenv("USERNAME") and data.get("password") == os.getenv("PWD"):
        # expires_delta=None znači da token NE ISTIČE
        token = create_access_token(identity=data["username"], expires_delta=None)
        return jsonify(access_token=token), 200
    return jsonify(msg="Bad credentials"), 401

# Pokretanje aplikacije (samo za lokalni razvoj)
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5100)
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token

import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET")  # nemanjica
jwt = JWTManager(app)


@app.route('/hello', methods=['GET'])
def hello():
    return jsonify({"message": "Zdravo iz Flask API-ja!"})

# ruta za login koja vraća token koji ne ističe
@app.route('/api/token', methods=['POST'])
def get_token():
    data = request.json
    # proverava korisničko ime i lozinku iz .env
    if data.get("username") == os.getenv("USERNAME") and data.get("password") == os.getenv("PWD"):
        # expires_delta=None znači da token NE ISTIČE
        token = create_access_token(identity=data["username"], expires_delta=None)
        return jsonify(access_token=token), 200
    return jsonify(msg="Bad credentials"), 401



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5100)
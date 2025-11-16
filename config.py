import os
from flask import Flask, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)

# =================== CORS CORRETO ===================
CORS(app,
     resources={r"/*": {"origins": [
         "http://localhost:3000",
         "https://clinica-miudesa-psi.vercel.app/"
     ]}},
     supports_credentials=True
)

# =================== HTTPS SEGURO (NÃO REDIRECIONAR OPTIONS) ===================
@app.before_request
def enforce_https():
    """Redirecionamento HTTP → HTTPS sem quebrar CORS"""
    if request.method == "OPTIONS":
        return  # NUNCA REDIRECIONAR OPTIONS

    is_https = (
        request.is_secure or 
        request.headers.get('X-Forwarded-Proto', 'https') == 'https'
    )

    if not is_https and 'localhost' not in request.host:
        https_url = request.url.replace('http://', 'https://', 1)
        return redirect(https_url, code=301)

# =================== CORS EXTRA PARA SEGURANÇA ===================
@app.after_request
def add_cors_headers(response):
    """Garante headers CORS em todas as respostas"""
    response.headers['Access-Control-Allow-Origin'] = "https://clinica-miudesa.vercel.app"
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    return response

# =================== BANCO ===================
db_path = os.path.join(os.getcwd(), "psicanalise.db")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JSON_SORT_KEYS"] = False

# =================== SERVIDOR ===================
app.config["HOST"] = "0.0.0.0"
app.config["PORT"] = 5000
app.config["DEBUG"] = True

# =================== INICIAR DB ===================
db = SQLAlchemy(app)

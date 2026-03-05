from flask import Flask
from flask_jwt_extended import JWTManager
from auth_routes import auth_bp
from ticket_routes import ticket_bp

app = Flask(__name__)

# JWT Configuration
app.config["JWT_SECRET_KEY"] = "your-secret-key-change-in-production"

jwt = JWTManager(app)

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(ticket_bp)

if __name__ == "__main__":
    app.run(debug=True)

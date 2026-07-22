from flask import Flask
from flask_cors import CORS

from routes.upload_routes import upload_bp
from routes.ask_routes import ask_bp
from routes.predict_routes import predict_bp
from routes.explorer_routes import explorer_bp
app = Flask(__name__)
CORS(app)

# Register Blueprints
app.register_blueprint(upload_bp)
app.register_blueprint(ask_bp)
app.register_blueprint(predict_bp)
app.register_blueprint(explorer_bp)

@app.route("/")
def home():
    return "OptiWise Backend Running "

if __name__ == "__main__":
   app.run(
    debug=True,
    use_reloader=False
)
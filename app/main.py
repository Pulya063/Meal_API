from flask import Flask
from app.db.database import engine, Base
from app.router.router import meal
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("APP_SECRET_KEY")

Base.metadata.create_all(bind=engine)
app.register_blueprint(meal, url_prefix='/')

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)

from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow requests from React frontend

@app.route('/')
def home():
    return {"message": "Flask backend is running!"}

if __name__ == "__main__":
    app.run(debug=True)


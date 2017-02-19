from app import app
from app.secrets import APP_PORT

if __name__ == "__main__":
    app.run(port=APP_PORT, host="0.0.0.0")

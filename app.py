from config import setup_config
from app import create_app

app = create_app(setup_config())


if __name__ == "__main__":
    app.run(debug=True, port=5000)

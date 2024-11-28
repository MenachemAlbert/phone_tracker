from flask import Flask

from app.routes.phone_tracker_route import phone_blueprint

app = Flask(__name__)

if __name__ == '__main__':
    app.register_blueprint(phone_blueprint, url_prefix="/api")
    app.run()

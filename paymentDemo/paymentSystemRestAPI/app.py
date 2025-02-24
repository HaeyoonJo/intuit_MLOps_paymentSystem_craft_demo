from flask import Flask
from payment_routes import payment_routes

app = Flask(__name__)
app.register_blueprint(payment_routes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
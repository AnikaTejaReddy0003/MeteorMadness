from flask import Flask, render_template
from neows.asteroid_loader import asteroid_data
from neows.neows import neows_bp
from apod.apod import apod_bp  # Add this import

app = Flask(__name__)


# Load data once when the app starts
def load_asteroid_data():
    asteroid_data.load_data("neows/asteroids.json")


load_asteroid_data()

# Register blueprints
app.register_blueprint(neows_bp)
app.register_blueprint(apod_bp)  # Add this line


@app.route('/')
def index():
    return render_template('homepage.html')


if __name__ == '__main__':
    app.run(debug=True)
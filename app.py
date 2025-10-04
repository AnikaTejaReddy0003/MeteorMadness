from flask import Flask, render_template
from apod.apod import apod_bp
import datetime


def create_app() -> Flask:
    app = Flask(__name__, template_folder='templates')
    app.register_blueprint(apod_bp)

    @app.context_processor
    def inject_globals():
        return {'current_year': datetime.datetime.now().year}

    @app.route('/')
    def index():
        return render_template('homepage.html')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

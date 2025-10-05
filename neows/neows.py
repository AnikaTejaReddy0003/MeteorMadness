from flask import Blueprint, render_template, request
from neows.asteroid_loader import asteroid_data

neows_bp = Blueprint('neows', __name__,
                     url_prefix='/neows',
                     template_folder='templates')


@neows_bp.route('/')
def list_asteroids():
    page = request.args.get('page', 1, type=int)
    per_page = 20  # Number of asteroids per page

    all_asteroids = asteroid_data.get_all_asteroids()
    total = len(all_asteroids)

    # Calculate pagination
    start = (page - 1) * per_page
    end = start + per_page
    asteroids = all_asteroids[start:end]

    # Calculate total pages
    total_pages = (total + per_page - 1) // per_page

    return render_template('neows.html',
                           asteroids=asteroids,
                           page=page,
                           total_pages=total_pages,
                           total=total)

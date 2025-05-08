from flask import Blueprint, render_template

# Create a Blueprint for serving the dashboard UI
#  - 'dashboard' is the blueprint name
#  - __name__ tells Flask where to find templates/static files
dashboard = Blueprint(
    'dashboard',           # Blueprint name for routing
    __name__,              # Module import name
    template_folder='templates'  # Folder where HTML templates reside
)

@dashboard.route('/')
def index():
    """
    Handle requests to the root URL ('/').

    :return: Rendered HTML template for the network dashboard
    """
    # Render 'dashboard.html' from the templates folder
    return render_template('dashboard.html')

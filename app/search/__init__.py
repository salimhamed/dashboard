from flask import Blueprint

# Create a Flask Blueprint which will define views and errors
search = Blueprint(
    'search',  # blueprint name
    __name__  # module where blueprint is located
)

# This Blueprint is defined as a Package named 'main'.  The modules imported
# below are part of the Blueprint.  The views and erros modules must be
# imported after the Blueprint object is instantiated because they rely on the
# Blueprint object to define routes and error handles
from . import views

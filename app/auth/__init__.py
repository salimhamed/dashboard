from flask import Blueprint

# Create a Flask Blueprint which will define views and errors
auth = Blueprint(
    'auth',  # blueprint name
    __name__  # module where blueprint is located
)

# This Blueprint is defined as a Package named 'auth'.  The modules imported
# below are part of the Blueprint.  The views module must be imported after
# the Blueprint object is instantiated because it relies on the Blueprint
# object to define routes
from . import views

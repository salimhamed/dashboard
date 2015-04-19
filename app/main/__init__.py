from flask import Blueprint

main = Blueprint(
    'main',  # blueprint name
    __name__  # module where blueprint is located
)

from . import views, errors

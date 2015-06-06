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


from .forms import SearchForm


# To avoid having to add a template argument in every 'render_template' call,
# the Search form is passed as a context processor.  This makes the
# Search form globally available to all templates.
@search.app_context_processor
def inject_search():
    return dict(SearchForm=SearchForm())

# This should be the base render class?
import utils.utils as jl_utils
import json

from django.conf import settings
class JupyterLabRender:
    def __init__(self):
        self.cells = None

    def generate_template_data(self, body):
        uuids = body['uuids']

        # Three implementations for templating

        # 1. JSON Template (example_template.json)
        # Loop over the json blob
        # Check the cell type to see whether it is a template cell
        # import utils, call that function dynamically
        # cells += function
        # Otherwise just use the src attribute from the template
        # cells += json['src']
        # Con: using this does not allow for conditional template generation
        # Pro & Con: Very very simple.

        # 2. Jinja Template (example_template.txt)
        # Make sure that util_functions are available within the Jinja context
        # Then we just call the django render function passing in the body and the template name
        # render('example_template.txt', body)
        # Pro: using this does allow for conditional template generation
        # Con: For JupterLab in particular, generating a valid JSON blob becomes complicated.

        # 3. Python
        # Go with a more module approach, that we are currently building towards
        # Template type "jupyter_lab" has a base class that:
        # a. Generates the "data" for the template.
        # b. Does the actual conversion from that "data" to the template format. IE JSON or string or CSV.
        # Pro: Huge level of flexibility.
        # Con: Non-technical user adoption will be near 0.

        self.cells = jl_utils.get_metadata_cells(uuids)
        self.cells += jl_utils.get_file_cells(uuids)
        self.cells += jl_utils.get_anndata_cells(uuids)

    def render(self):
        # We should append the cells
        nb = {
           'cells': self.cells,
            'metadata': {},
            'nbformat': 4,
            'nbformat_minor': 5
        }

        return json.dumps(nb)
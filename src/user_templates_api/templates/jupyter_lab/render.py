import json

class JupyterLabRender:

    def render(self, data):
        # We should append the cells
        # TODO: Check for the template format in metadata.json
        #  and use the appropriate method.

        metadata = data['metadata']

        if metadata['template_format'] == 'python':
            cells = self.python_generate_template_data(data)
        elif metadata['template_format'] == 'json':
            cells = self.json_generate_template_data(data)

        nb = {
            'cells': cells,
            'metadata': {},
            'nbformat': 4,
            'nbformat_minor': 5
        }

        return json.dumps(nb)

    def python_generate_template_data(self, data):
        return []

    def json_generate_template_data(self, data):
        uuids = data['body']['uuids']
        # TODO: # 1. JSON Template (example_template.json)
        #         # Loop over the json blob
        #         # Check the cell type to see whether it is a template cell
        #         # import utils, call that function dynamically
        #         # cells += function
        #         # Otherwise just use the src attribute from the template
        #         # cells += json['src']
        #
        return []
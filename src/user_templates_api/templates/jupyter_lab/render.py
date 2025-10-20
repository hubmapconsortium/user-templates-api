import inspect
import json
from pathlib import Path

from django.template import engines

from user_templates_api.templates.jupyter_lab.utils.convert_templates.convert_notebook import (
    conversion,
)

# from nbformat.v4 import new_code_cell, new_markdown_cell
# import user_templates_api.templates.jupyter_lab.utils.utils as jl_utils


class JupyterLabRender:
    def render(self, data):
        metadata = data["metadata"]
        data["uuids"] = data.get("uuids", [])

        if metadata["template_format"] != "jinja":
            return

        cells = self.jinja_generate_template_data(data)

        nb = {"cells": cells, "metadata": {}, "nbformat": 4, "nbformat_minor": 5}

        return json.dumps(nb)

    def jinja_generate_template_data(self, data):
        django_engine = engines["django"]

        # Get the file path first
        class_file_path = inspect.getfile(self.__class__)
        # Convert the string to a pathlib Path
        class_file_path = Path(class_file_path)
        # Grab the parent path and append template.txt
        template_file_path = class_file_path.parent / "template.ipynb"
        # Load that filepath since it should be the json template
        template_file = open(template_file_path)
        template = django_engine.from_string(conversion(template_file.read()))
        rendered_template = template.render(data).strip()
        rendered_template = json.loads(rendered_template) if rendered_template else {}

        # Update this so that it returns actual JSON not text
        return rendered_template

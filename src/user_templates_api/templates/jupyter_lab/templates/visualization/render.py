import vitessce
from nbformat.v4 import new_code_cell, new_markdown_cell

from user_templates_api.templates.jupyter_lab.render import JupyterLabRender
from user_templates_api.utils.client import get_client


class JupyterLabVisualizationRender(JupyterLabRender):
    def python_generate_template_data(self, data):
        uuids = data["body"]["uuids"]
        uuid = uuids[0]

        client = get_client(data["group_token"])
        entity = client.get_entity(uuid)
        vitessce_conf = client.get_vitessce_conf_cells_and_lifted_uuid(
            entity
        ).vitessce_conf
        if (
            vitessce_conf is None
            or vitessce_conf.conf is None
            or vitessce_conf.cells is None
        ):
            vitessce_conf.cells = new_markdown_cell(
                "## Error in visualization\n"
                f"Vitessce visualization could not be displayed for dataset {uuid}."
            )

        cells = [
            new_markdown_cell(
                "# Vitessce visualization for single dataset\n"
                "This notebook shows a Vitessce visualization for a dataset."
            ),
            new_code_cell(
                "!pip uninstall community flask albumentations -y "
                "# Preinstalled on Colab; Causes version conflicts.\n"
                f"!pip install vitessce[all]=={vitessce.__version__}"
            ),
            new_markdown_cell(
                "## Linked datasets\n"
                "For this template, symlinking is not required. "
                "This template only visualizes one dataset, it will automatically select the first of the datasets."
            ),
            *vitessce_conf.cells,
        ]

        return cells

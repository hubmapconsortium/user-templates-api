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

        hubmap_id = entity["hubmap_id"]
        cells = [
            new_markdown_cell(
                f"Visualization for {hubmap_id}; "
                "If this notebook is running in a HuBMAP workspace, the dataset is symlinked:"
            ),
            new_code_cell(f"!ls datasets/{uuids}"),
            new_markdown_cell("Visualization requires extra code to be installed:"),
            new_code_cell(
                "!pip uninstall community flask albumentations -y "
                "# Preinstalled on Colab; Causes version conflicts.\n"
                f"!pip install vitessce[all]=={vitessce.__version__}"
            ),
            *vitessce_conf.cells,
        ]

        return cells

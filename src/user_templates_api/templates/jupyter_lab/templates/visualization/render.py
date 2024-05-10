from importlib_metadata import version
from nbformat.v4 import new_code_cell, new_markdown_cell

from user_templates_api.templates.jupyter_lab.render import JupyterLabRender
from user_templates_api.utils.client import get_client


class JupyterLabVisualizationRender(JupyterLabRender):
    def python_generate_template_data(self, data):
        uuids = data["uuids"]
        uuid = uuids[0]

        client = get_client(data["group_token"])
        entity = client.get_entity(uuid)
        vitessce_conf = client.get_vitessce_conf_cells_and_lifted_uuid(
            entity
        ).vitessce_conf

        if not vitessce_conf or not vitessce_conf.conf or not vitessce_conf.cells:
            vitessce_conf.cells.append(
                new_markdown_cell(
                    "## Error in visualization\n"
                    f"Vitessce visualization could not be displayed for dataset {uuid}."
                )
            )

        cells = [
            new_markdown_cell(
                "# Vitessce visualization for single dataset\n"
                "This notebook shows a Vitessce visualization for a dataset."
            ),
            new_code_cell(
                f"!pip install vitessce[all]=={version('vitessce')}"
            ),
            new_markdown_cell(
                "## Linked datasets\n"
                "For this template, symlinking is not required. "
                "This template only visualizes one dataset, it will automatically select the first of the datasets."
            ),
            *vitessce_conf.cells,
            new_code_cell(
                "## If you get a JavaScript error when running the above cell, it is likely due \n",
                "## to Anywidget needing to be installed before the workspace is launched.\n",
                "\n",
                "## Check that anywidget is installed\n",
                "## Uncomment the following line:\n",
                "# import anywidget \n",
                "\n",
                "## If it is not yet installed:\n",
                "# !pip install anywidget\n",
                "\n",
                "## Once you have checked that it is installed, close this window.\n",
                "## In the Workspace overview page, stop all jobs.\n",
                "## Then, launch the Workspace again."
            ),
        ]

        return cells

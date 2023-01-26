import nbformat
from nbformat.v4 import (new_notebook, new_markdown_cell, new_code_cell)
import vitessce

def render(body, util_client):
    uuid = body['uuid']
    entity = util_client.get_entity(uuid)
    vitessce_conf = util_client.get_vitessce_conf_cells_and_lifted_uuid(entity).vitessce_conf
    if (vitessce_conf is None
            or vitessce_conf.conf is None
            or vitessce_conf.cells is None):
        return {'success': False, 'message': 'Vitessce conf not found.'}

    hubmap_id = entity['hubmap_id']
    cells = [
        new_markdown_cell(
            f"Visualization for {hubmap_id}; "
            "If this notebook is running in a HuBMAP workspace, the dataset is symlinked:"),
        new_code_cell(f'!ls datasets/{uuid}'),
        new_markdown_cell('Visualization requires extra code to be installed:'),
        new_code_cell(
            '!pip uninstall community flask albumentations -y '
            '# Preinstalled on Colab; Causes version conflicts.\n'
            f'!pip install vitessce[all]=={vitessce.__version__}'),
        *vitessce_conf.cells
    ]

    nb = new_notebook()
    nb['cells'] = cells
    nb_str = nbformat.writes(nb)

    return nb_str

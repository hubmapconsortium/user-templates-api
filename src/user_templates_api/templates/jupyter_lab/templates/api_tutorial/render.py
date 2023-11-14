import user_templates_api.templates.jupyter_lab.utils.utils as jl_utils
from user_templates_api.templates.jupyter_lab.render import JupyterLabRender
from user_templates_api.utils.client import get_client


class JupyterLabAPITutorialRender(JupyterLabRender):
    def python_generate_template_data(self, data):
        uuids = data["uuids"]

        util_client = get_client(data["group_token"])

        cells = jl_utils.get_metadata_cells(uuids, util_client)
        cells += jl_utils.get_file_cells(uuids, util_client)
        cells += jl_utils.get_anndata_cells(uuids, util_client)
        return cells

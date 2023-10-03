import user_templates_api.templates.jupyter_lab.utils.utils as jl_utils
from user_templates_api.templates.jupyter_lab.render import JupyterLabRender
from user_templates_api.utils.client import get_client


class JupyterLabExampleJSONRender(JupyterLabRender):
    def __init__(self):
        pass


# class JupyterLabAPITutorialRender(JupyterLabRender):
#     def python_generate_template_data(self, data):
#         uuids = data["body"]["uuids"]
#         util_client = get_client(data["group_token"])

#         cells = jl_utils._get_cells("template.txt", uuids, util_client)
#         return cells
from user_templates_api.templates.jupyter_lab.render import JupyterLabRender


class JupyterLabExampleJSONRender(JupyterLabRender):
    def __init__(self):
        pass

# class JupyterLabAPITutorialRender(JupyterLabRender):
#     def python_generate_template_data(self, data):
#         uuids = data["body"]["uuids"]
#         util_client = get_client(data["group_token"])

#         cells = jl_utils._get_cells("template.txt", uuids, util_client)
#         return cells
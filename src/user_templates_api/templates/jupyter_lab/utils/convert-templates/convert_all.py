import os
import json

from convert_notebook import notebookToTxt, txtToNotebook

templates_folder = "src/user_templates_api/templates/jupyter_lab/templates"

templates = os.listdir(templates_folder)
templates_jinja = []

# retrieve templates that are jinja format
for template in templates:
    if not os.path.isdir(f"{templates_folder}/{template}"):
        continue
    with open(f"{templates_folder}/{template}/metadata.json", "r") as file:
        metadata = json.load(file)
        if metadata.get("template_format", "") == "jinja" and metadata.get("is_hidden", "") == False:
            templates_jinja.append(template)
   

for template in templates_jinja:
    print(template)
    txtToNotebook(template)
    notebookToTxt(template)

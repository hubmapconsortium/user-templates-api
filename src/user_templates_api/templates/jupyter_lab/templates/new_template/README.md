# Adding new template
We welcome template contributions!

Each template has it's own folder in [src/user_templates_api/templates/jupyter_lab/templates](https://github.com/hubmapconsortium/user-templates-api/tree/development/src/user_templates_api/templates/jupyter_lab/templates). To add a new template, copy this folder or add a new folder with 4 files: 
- README.md
- metadata.json
- render.py
- template.txt 
Use short, descriptive words for the folder name.

## README.md
The README contains further information about the template. At least include 1 dataset (for single dataset templates) or 3 datasets (for multi dataset templates) that work with this template.


## metadata.json
The metadata.json is used to display the templates in the HuBMAP Data Portal. It consists of: 
- title: a title of the notebook.
- description: a 1-2 sentence description of the notebook.
- tags: a list of tags to describe the notebook. Potential tags can be found [here](https://github.com/hubmapconsortium/user-templates-api/tree/development/src/tags.json). New tags can be added if necessary. In future releases, any template with the 'test' tag is not shown in the portal.
- is_multi_dataset_template: boolean describing whether template can handle more than 1 dataset
- template_format: one of python/json/jinja. We recommend using jinja, and describe the insertion of cells for jinja below.


## render.py
For the jinja format, the render.py as in this folder is sufficient.


## template.txt
The actual template. This can be directly converted from .ipynb to .txt. If insertion of values is required, e.g. uuids, add any of the \_get_\[...]_cells in [utils.py](https://github.com/hubmapconsortium/user-templates-api/blob/development/src/user_templates_api/templates/jupyter_lab/utils/utils.py) as follows: 
```sh
{% jupyter_get_uuid_cells %}
```
An example can be found in the compress_anndata template.

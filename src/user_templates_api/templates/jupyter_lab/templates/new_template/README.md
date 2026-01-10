# Adding new template
We welcome template contributions!

Each template has it's own folder in [src/user_templates_api/templates/jupyter_lab/templates](https://github.com/hubmapconsortium/user-templates-api/tree/development/src/user_templates_api/templates/jupyter_lab/templates). To add a new template, copy this folder or add a new folder with 4 files: 
- README.md
- metadata.json
- render.py
- template.txt <- this was the previous way we handled templates, but is not necessary anymore.
- template.ipynb

Use short, descriptive words for the folder name.

## README.md
The README contains further information about the template. At least include 1 dataset (for single dataset templates) or 3 datasets (for multi dataset templates) that work with this template.


## metadata.json
The metadata.json is used to display the templates in the HuBMAP Data Portal. It consists of: 
- `title`: a title of the notebook.
- `description`: a 1-2 sentence description of the notebook.
- `tags`: a list of tags to describe the notebook. Potential tags can be found [here](https://github.com/hubmapconsortium/user-templates-api/tree/development/src/tags.json). New tags can be added if necessary. 
- `is_multi_dataset_template`: boolean describing whether template can handle more than 1 dataset.
- `template_format`: one of `python`/`json`/`jinja`. We recommend using `jinja`, and describe the insertion of cells for jinja below.
- `examples`: array with examples that are shown in the template example pages. Each example has a `title` (string), a `description` (string), and `datasets` (array of strings). These datasets are a list of uuids of [public, published datasets on the HuBMAP Data Portal](https://portal.hubmapconsortium.org/search?mapped_status_keyword-mapped_data_access_level_keyword[Published][0]=Public&entity_type[0]=Dataset). Optionally, it also has an `assay_display_name` (array) with the possible assay_display_names, and `required_filetypes` (array) with required filetypes.
- `contributors`: array with contributors. Each contributor has a `name`, `affiliation`, `orcid`, `github_id`, `email`. All should have a `name` and `affiliation`, the other fields are optional.
- `is_hidden`: Any template with this field set to `true` is not shown in the Portal.
- `last_modified_unix_timestamp`: Don't set this, it is added automatically to keep track of changes.


## render.py
For the jinja format, the render.py as in this folder is sufficient.


## template.ipynb
The actual template. 

If insertion of values is required, e.g. uuids, you can add them as follows: 
```sh
uuids = {{ uuids | safe }}
```
An example can be found in the blank template.


If you are working with an older template and want to convert this to a notebook again, you can use the script [here](https://github.com/hubmapconsortium/user-templates-api/blob/development/src/user_templates_api/templates/jupyter_lab/utils/convert_templates/README.md).

This script is run as follows for e.g. the blank example. `tonb` converts .txt to .ipynb, `totxt` converst .ipynb to .txt.

```sh
python src/user_templates_api/templates/jupyter_lab/utils/convert_templates/convert_notebook.py tonb blank
python src/user_templates_api/templates/jupyter_lab/utils/convert_templates/convert_notebook.py totxt blank
```

## Helper package
A few functions that help with creating templates, such as a template compatibility checker, are included in a small helper package. Install it as such:

```sh
pip install hubmap-template-helper
```

Read more [here](https://github.com/thomcsmits/hubmap_template_helper).

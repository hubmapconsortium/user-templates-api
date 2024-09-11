# user-templates-api
This repository handles templates for the [workspaces feature](https://portal.hubmapconsortium.org/workspaces) in the HuBMAP Data Portal. Templates are pre-set notebooks with analyses that can be added to a workspace. Variables linked to a workspace (such as the datasets added to the workspace) can be added into the templates.


## Contributing
We welcome contributions! Please see our [contributing guidelines](https://github.com/hubmapconsortium/user-templates-api/blob/development/CONTRIBUTING.md). For adding new templates, please see our [template contributing guidelines](https://github.com/hubmapconsortium/user-templates-api/blob/development/src/user_templates_api/templates/jupyter_lab/templates/new_template/README.md). 

We also have a slack channel for feedback on the workspaces. Please reach out to the HuBMAP Help Desk ([help@hubmapconsortium.org](mailto:help@hubmapconsortium.org)) to get in touch.

## Deploying User Templates Locally
- Clone the repository.
- Generate a virtual environment (`virtualenv -p python3.9 venv`).
- Activate the virtual environment (`source venv/bin/activate`).
- Install the requirements (`pip install -r requirements.txt`).
- Create a config file (`cp src/example_config.json src/config.json`) and update it with appropriate values.
- Run database migration (`python src/manage.py migrate`).
- Start the server (`python src/manage.py runserver`).


## Contributors
This project is part of the HuBMAP consortium. The main contributors to the workspaces are the [Pittsburgh Supercomputing Center](https://www.psc.edu/) and the [HIDIVE Lab](https://hidivelab.org) at [Harvard Medical School](https://hms.harvard.edu).

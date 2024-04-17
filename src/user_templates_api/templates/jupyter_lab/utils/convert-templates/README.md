# Convertion between txt and Jupyter notebooks
This folder contains a helper script to convert between txt and ipynb files. 

In the txt files, there should only be a list of the cells included. In the ipynb files, there is a wrapper with "cells" and some information at the bottom. 

Using the script in this folder, one can easily convert between either.

There are two parameters that need to be supplied: 
1. The option. Either 'totxt' to convert ipynb to txt, or 'tonb' to convert txt to ipynb.
2. The folder. The name of the folder in which the files are located. Don't include the entire path. E.g. `squidpy` or `celltypes_salmon`.

Run it as follows: 

```sh
python3 src/user_templates_api/templates/jupyter_lab/utils/convert-templates/convert-notebook.py OPTION FOLDER
```
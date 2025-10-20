import json
import sys


def getTemplatePath():
    """
    Function returning the path of the templates folder.
    """
    return "./src/user_templates_api/templates/jupyter_lab/templates"


def txtToNotebook(file_folder):
    """
    Function that converts a .txt file into a .ipynb file.
    Parameters
    ----------
    file_folder : str
        Name of the folder (without it's path), e.g. 'celltypes_salmon'
    """
    # get paths
    template_path = getTemplatePath()
    file_name_txt = f"{template_path}/{file_folder}/template.txt"
    file_name_ipynb = f"{file_name_txt.split('.txt')[0]}.ipynb"

    # read txt
    text_txt = []
    with open(file_name_txt, "r") as file:
        text_txt = [f for f in file.readlines()]

    # append start and end to txt
    text_ipynb = []
    text_ipynb.append("{\n")
    text_ipynb.append(' "cells": ')
    for line in text_txt:
        text_ipynb.append(f"{line}")

    for line in [
        ",\n",
        ' "metadata": {\n',
        '  "language_info": {\n',
        '   "name": "python"\n',
        "  }\n",
        " },\n",
        ' "nbformat": 4,\n',
        ' "nbformat_minor": 2\n',
        "}",
    ]:
        text_ipynb.append(line)

    # write as ipynb
    with open(file_name_ipynb, "w") as file:
        file.writelines(text_ipynb)


def notebookToTxt(file_folder):
    """
    Function that converts a .ipynb file into a .txt file.
    Parameters
    ----------
    file_folder : str
        Name of the folder (without it's path), e.g. 'celltypes_salmon'
    """
    # get paths
    template_path = getTemplatePath()
    file_name_ipynb = f"{template_path}/{file_folder}/template.ipynb"
    file_name_txt = f"{file_name_ipynb.split('.ipynb')[0]}.txt"

    # read ipynb
    with open(file_name_ipynb, "r") as file:
        js = json.load(file)
   
    cells = js.get("cells", [])

    # remove metadata, execution_count, outputs, id
    for cell in cells: 
        if "metadata" in cell.keys():
            cell["metadata"] = {}
        if "execution_count" in cell.keys():
            cell["execution_count"] = None
        if "outputs" in cell.keys():
            cell["outputs"] = []
        if "id" in cell.keys():
            cell.pop("id")
    
    with open(file_name_txt, "w") as file:
        json.dump(cells, file, indent=2)


try:
    option = sys.argv[1]
    file_folder = sys.argv[2]

    if option == "totxt":
        notebookToTxt(file_folder)
    if option == "tonb":
        txtToNotebook(file_folder)

except IndexError:
    raise Warning(
        "Did you supply two arguments? The first is 'totxt' or 'nb', the second is the folder name."
    )

except FileNotFoundError:
    raise Warning("Did you supply a valid template folder? Otherwise check the path")

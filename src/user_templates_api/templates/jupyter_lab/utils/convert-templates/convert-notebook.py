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

    # read ipynb as json
    with open(file_name_ipynb, "r") as file:
        text_ipynb = json.loads(file.read())

    # replace execution count with null and outputs with empty
    text_ipynb = text_ipynb["cells"]
    for cell in text_ipynb:
        if cell["cell_type"] == "code":
            cell["execution_count"] = None
            cell["metadata"] = {}
            cell["outputs"] = []

    # write as txt
    # add spacing as in .ipynb
    text_ipynb_str = json.dumps(text_ipynb, indent=1)
    text_ipynb_str_list = text_ipynb_str.split("\n")
    for i, l in enumerate(text_ipynb_str_list):
        if i != 0 and i != len(text_ipynb_str_list) - 1:
            text_ipynb_str_list[i] = f" {l}"
    text_ipynb_combined = "\n".join(text_ipynb_str_list)
    print(text_ipynb_combined)

    # write to txt
    with open(file_name_txt, "w") as file:
        file.write(text_ipynb_combined)


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

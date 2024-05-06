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
    text_ipynb = []
    with open(file_name_ipynb, "r") as file:
        text_ipynb = file.read()

    # extract everything between the cells list
    # this is everything between the first bracket and its closing bracket
    opened = 0
    closed = 0
    text_txt_chars = ""
    for char in text_ipynb:
        if char == "[":
            opened += 1
        if opened > 0:
            if opened != closed:
                text_txt_chars += char
        if char == "]":
            closed += 1

    # add back newline characters
    text_txt_list = [f"{line}\n" for line in text_txt_chars.split("\n")]

    # replace execution count with null and outputs with empty
    for i in range(len(text_txt_list)):
        if '"execution_count":' in text_txt_list[i]:
            text_txt_list[i] = '   "execution_count": null,\n'
        if '"outputs":' in text_txt_list[i]:
            text_txt_list[i] = '   "outputs": [],\n'

    # write to txt
    with open(file_name_txt, "w") as file:
        file.writelines(text_txt_list)


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

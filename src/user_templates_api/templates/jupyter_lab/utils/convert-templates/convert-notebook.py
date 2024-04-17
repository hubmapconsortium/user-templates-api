import sys

def txtToNotebook(file_folder): 
    file_name_txt = f"./src/user_templates_api/templates/jupyter_lab/templates/{file_folder}/template.txt"
    file_name_ipynb = f"{file_name_txt.split('.txt')[0]}.ipynb"

    text_txt = []
    with open(file_name_txt, "r") as file: 
        text_txt = [f for f in file.readlines()]

    text_ipynb = []
    text_ipynb.append('{\n')
    text_ipynb.append(' "cells": ')
    for line in text_txt:
        text_ipynb.append(f"{line}")

    for line in [',\n', ' "metadata": {\n', '  "language_info": {\n', '   "name": "python"\n', '  }\n', ' },\n', ' "nbformat": 4,\n', ' "nbformat_minor": 2\n', '}']:
        text_ipynb.append(line)

    with open(file_name_ipynb, "w") as file: 
        file.writelines(text_ipynb)

file_folder = sys.argv[1]
txtToNotebook(file_folder)
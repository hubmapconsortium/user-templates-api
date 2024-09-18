import json
import os

# read in the existing tags in tags.json
with open("./src/tags.json") as file:
    tags_dict = json.load(file)

tags = list(tags_dict.keys())
tags.sort()

# retrieve all tags used in templates
templates_path = "./src/user_templates_api/templates/jupyter_lab/templates/"
templates = os.listdir(templates_path)

template_tags = []
for template in templates:
    with open(templates_path + template + "/metadata.json") as file:
        metadata = json.load(file)
        if not metadata["is_hidden"]:
            template_tags.extend(metadata["tags"])

template_tags = list(set(template_tags))
template_tags.sort()

# check if all tags used in templates are part of tags.json
missing_tags = [tag for tag in template_tags if tag not in tags]

if len(missing_tags) > 1:
    raise ValueError(
        f"All tags in templates should exist in tags.json. The following tags are missing in tags.json: {missing_tags}"
    )

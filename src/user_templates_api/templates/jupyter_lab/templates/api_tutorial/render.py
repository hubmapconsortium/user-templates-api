import json
import re
from pathlib import Path
from string import Template

from django.conf import settings


def render(body, util_client):
    uuids = body["uuids"]
    entity_type = body["entity_type"]

    url_base = settings.CONFIG["PORTAL_UI_BASE"]

    cells = _get_cells(
        "metadata.txt", uuids=uuids, url_base=url_base, entity_type=entity_type
    )

    if entity_type == "datasets":
        search_url = (
            settings.CONFIG["ELASTICSEARCH_ENDPOINT"]
            + settings.CONFIG["PORTAL_INDEX_PATH"]
        )
        cells += _get_cells("files.txt", search_url=search_url)

    uuids_to_files = util_client.get_files(uuids)
    uuids_to_zarr_files = _limit_to_zarr_files(uuids_to_files)
    zarr_files = set().union(*uuids_to_zarr_files.values())
    if zarr_files:
        cells += _get_cells("anndata.txt", uuids_to_zarr_files=uuids_to_zarr_files)

    nb = {"cells": cells, "metadata": {}, "nbformat": 4, "nbformat_minor": 5}

    return json.dumps(nb)


def _limit_to_zarr_files(uuids_to_files):
    """
    >>> uuids_to_files = {'1234': ['asdf/.zarr/abc', 'asdf/.zarr/xyz', 'other']}
    >>> _limit_to_zarr_files(uuids_to_files)
    {'1234': {'asdf/.zarr'}}
    """
    return {
        uuid: set(re.sub(r"\.zarr/.*", ".zarr", f) for f in files if ".zarr" in f)
        for uuid, files in uuids_to_files.items()
    }


def _get_cells(filename, **kwargs):
    template = Template((Path(__file__).parent / "notebook" / filename).read_text())
    filled = template.substitute(kwargs)
    return json.loads(filled)["cells"]

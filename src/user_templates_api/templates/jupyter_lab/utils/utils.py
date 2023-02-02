import json
import re
from pathlib import Path
from string import Template

from django.conf import settings


def get_metadata_cells(uuids, util_client):
    url_base = settings.CONFIG["PORTAL_UI_BASE"]
    #  Need to get the uuids entity_type to pass it
    entity_type = "dataset"
    return _get_cells(
        "metadata.txt", uuids=uuids, url_base=url_base, entity_type=entity_type
    )


def get_file_cells(uuids, util_client):
    # TODO: Need to check that these uuids are dataset uuids
    search_url = (
        settings.CONFIG["ELASTICSEARCH_ENDPOINT"] + settings.CONFIG["PORTAL_INDEX_PATH"]
    )
    return _get_cells("files.txt", search_url=search_url)


def get_anndata_cells(uuids, util_client):
    uuids_to_files = util_client.get_files(uuids)
    uuids_to_zarr_files = _limit_to_zarr_files(uuids_to_files)
    zarr_files = set().union(*uuids_to_zarr_files.values())
    return (
        _get_cells("anndata.txt", uuids_to_zarr_files=uuids_to_zarr_files)
        if zarr_files
        else []
    )


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

from django import template
import user_templates_api.templates.jupyter_lab.utils.utils as jl_utils

register = template.Library()


@register.simple_tag(takes_context=True)
def jupyter_get_metadata_cells(context):
    uuids = context["body"]["uuids"]
    util_client = context["util_client"]
    cells = jl_utils.get_metadata_cells(uuids, util_client)
    cells_str = str(cells)
    cells_str = cells_str[1:-1]
    return cells_str


@register.simple_tag(takes_context=True)
def jupyter_get_file_cells(context):
    uuids = context["body"]["uuids"]
    util_client = context["util_client"]
    cells = jl_utils.get_file_cells(uuids, util_client)
    cells_str = str(cells)
    cells_str = cells_str[1:-1]
    return cells_str


@register.simple_tag(takes_context=True)
def jupyter_get_anndata_cells(context):
    uuids = context["body"]["uuids"]
    util_client = context["util_client"]
    cells = jl_utils.get_anndata_cells(uuids, util_client)
    if not cells:
        return ""
    cells_str = str(cells)
    cells_str = cells_str[1:-1]
    return cells_str

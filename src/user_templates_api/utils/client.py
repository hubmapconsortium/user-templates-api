from django.conf import settings
from portal_visualization.client import ApiClient


# TODO: Need to rewrite some of this so that it doesn't use flask.


def get_client(group_token):
    return ApiClient(
        groups_token=group_token,
        elasticsearch_endpoint=settings.CONFIG["ELASTICSEARCH_ENDPOINT"],
        portal_index_path=settings.CONFIG["PORTAL_INDEX_PATH"],
        ubkg_endpoint=settings.CONFIG["UBKG_ENDPOINT"],
        assets_endpoint=settings.CONFIG["ASSETS_ENDPOINT"],
        soft_assay_endpoint=settings.CONFIG["SOFT_ASSAY_ENDPOINT"],
        soft_assay_endpoint_path=settings.CONFIG["SOFT_ASSAY_ENDPOINT_PATH"],
        entity_api_endpoint=settings.CONFIG["ENTITY_API_BASE"],
    )

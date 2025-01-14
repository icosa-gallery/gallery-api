from typing import Any, List, Optional

from icosa.api.authentication import AuthBearer
from ninja import Schema
from ninja.pagination import PaginationBase

from django.db.models import Q

COMMON_ROUTER_SETTINGS = {
    "exclude_none": True,
    "exclude_defaults": True,
}

POLY_CATEGORY_MAP = {
    "TECHNOLOGY": "TECH",
}

DEFAULT_PAGE_SIZE = 20
DEFAULT_PAGE_TOKEN = 1
MAX_PAGE_SIZE = 100


class AssetPagination(PaginationBase):
    class Input(Schema):
        pageToken: str = None
        page_token: str = None
        pageSize: str = None
        page_size: str = None

    class Output(Schema):
        assets: List[Any]
        totalSize: int
        nextPageToken: Optional[str] = None

    items_attribute: str = "assets"

    def paginate_queryset(
        self, queryset, pagination: Input, request, **params
    ):
        try:
            page_size = (
                int(pagination.pageSize)
                or int(pagination.page_size)
                or DEFAULT_PAGE_SIZE
            )
        except (ValueError, TypeError):
            # pageSize could still be defined, but empty: `?pageSize=`).
            page_size = DEFAULT_PAGE_SIZE
        page_size = min(page_size, MAX_PAGE_SIZE)

        try:
            page_token = (
                int(pagination.pageToken)
                or int(pagination.page_token)
                or DEFAULT_PAGE_TOKEN
            )
        except (ValueError, TypeError):
            # pageToken could still be defined, but empty: `?pageToken=`).
            page_token = DEFAULT_PAGE_TOKEN

        offset = (page_token - 1) * page_size
        count = self._items_count(queryset)
        if type(queryset) == list:
            queryset_count = len(queryset)
        else:
            queryset_count = queryset.count()
        pagination_data = {
            "assets": queryset[offset : offset + page_size],
            "totalSize": queryset_count,
        }
        if offset + page_size < count:
            pagination_data.update(
                {
                    "nextPageToken": str(page_token + 1),
                }
            )
        return pagination_data


def build_format_q(formats: List) -> Q:
    q = Q()
    if "TILT" in formats:
        q &= Q(has_tilt=True)
    if "BLOCKS" in formats:
        q &= Q(has_blocks=True)
    if "GLTF" in formats:
        q &= Q(has_gltf_any=True)
    if "GLTF1" in formats:
        q &= Q(has_gltf1=True)
    if "GLTF2" in formats:
        q &= Q(has_gltf2=True)
    if "OBJ" in formats:
        q &= Q(has_obj=True)
    if "FBX" in formats:
        q &= Q(has_fbx=True)
    return q


def get_django_user_from_auth_bearer(request):
    header = request.headers.get("Authorization")
    if header is None:
        return None
    if not header.startswith("Bearer "):
        return None
    token = header.replace("Bearer ", "")
    return AuthBearer().authenticate(request, token)

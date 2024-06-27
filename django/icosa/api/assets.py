import re
from typing import List, NoReturn, Optional

from icosa.models import PUBLIC, Asset, Tag, User
from ninja import Query, Router
from ninja.errors import HttpError
from ninja.files import UploadedFile
from ninja.pagination import paginate

from django.db.models import Q
from django.http import HttpRequest

from .authentication import AuthBearer
from .schema import AssetFilters, AssetSchemaOut

router = Router()


IMAGE_REGEX = re.compile("(jpe?g|tiff?|png|webp|bmp)")


def user_can_view_asset(
    request: HttpRequest,
    asset: Asset,
) -> bool:
    if asset.visibility == "PRIVATE":
        return user_owns_asset(request, asset)
    return True


def user_owns_asset(
    request: HttpRequest,
    asset: Asset,
) -> bool:
    if (
        request.auth.is_anonymous
        or User.from_ninja_request(request) != asset.owner
    ):
        return False
    return True


def check_user_owns_asset(
    request: HttpRequest,
    asset: Asset,
) -> NoReturn:
    if not user_owns_asset(request, asset):
        raise HttpError(403, "Unauthorized user.")


def get_asset_by_id(
    request: HttpRequest,
    asset: int,
) -> Asset:
    # get_object_or_404 raises the wrong error text
    try:
        asset = Asset.objects.get(pk=asset)
    except Asset.DoesNotExist:
        raise HttpError(404, "Asset not found.")
    if not user_can_view_asset(request, asset):
        raise HttpError(404, "Asset not found.")
    return asset


def get_my_id_asset(
    request,
    asset: int,
):
    try:
        asset = get_asset_by_id(request, asset)
    except Exception:
        raise
    check_user_owns_asset(request, asset)
    return asset


def remove_folder_gcs(folder_path):
    """Remove entire folder from bucket."""
    # TODO(james): do we wait until storages is implemented for this?
    return False
    # storage_client = storage.Client.from_service_account_json(
    #     data["service_account_data"]
    # )
    # blobs = storage_client.list_blobs(
    #     data["gcloud_bucket_name"], prefix=folder_path
    # )
    # for blob in blobs:
    #     try:
    #         blob.delete()
    #     except Exception as e:
    #         print(e)
    #         return False
    # return True


@router.get(
    "/id/{asset}",
    response=AssetSchemaOut,
)
def get_id_asset(
    request,
    asset: int,
):
    return get_asset_by_id(request, asset)


@router.delete(
    "/{asset}",
    auth=AuthBearer(),
    response=AssetSchemaOut,
)
def delete_asset(
    request,
    asset: int,
):
    asset = get_my_id_asset(request, asset)
    # TODO(james): do we wait until storages is implemented for this?
    # asset.delete()
    # Asset removal from storage
    owner = User.from_ninja_request(request)
    asset_folder = f"{owner.id}/{asset}/"
    if not (remove_folder_gcs(asset_folder)):
        print(f"Failed to remove asset {asset}")
        raise HttpError(
            status_code=500, detail=f"Failed to remove asset {asset}"
        )
    return asset


# TODO(james): do we wait until storages is implemented for this?
# @router.patch(
#     "/{asset}",
#     auth=AuthBearer(),
#     response_model=Asset,
# )
# def update_asset(
#     request
#     background_tasks: BackgroundTasks,
#     request: Request,
#     asset: int,
#     data: Optional[AssetPatchData] = None,
#     name: Optional[str] = Form(None),
#     url: Optional[str] = Form(None),
#     description: Optional[str] = Form(None),
#     visibility: Optional[str] = Form(None),
#     current_user: User = Depends(get_current_user),
#     thumbnail: Optional[UploadedFile] = File(None),
# ):
#     current_asset = _DBAsset(**(await get_my_id_asset(asset, current_user)))

#     if request.headers.get("content-type") == "application/json":
#         update_data = data.dict(exclude_unset=True)
#     elif request.headers.get("content-type").startswith("multipart/form-data"):
#         update_data = {
#             k: v
#             for k, v in {
#                 "name": name,
#                 "url": url,
#                 "description": description,
#                 "visibility": visibility,
#             }.items()
#             if v is not None
#         }
#     else:
#         raise HTTPException(
#             status_code=415, detail="Unsupported content type."
#         )

#     updated_asset = current_asset.copy(update=update_data)
#     updated_asset.id = int(updated_asset.id)
#     updated_asset.owner = int(updated_asset.owner)
#     query = assets.update(None)
#     query = query.where(assets.c.id == updated_asset.id)
#     query = query.values(updated_asset.dict())
#     await database.execute(query)
#     if thumbnail:
#         background_tasks.add_task(
#             upload_thumbnail_background, current_user, thumbnail, asset
#         )
#     return await get_my_id_asset(asset, current_user)


@router.patch(
    "/{str:asset}/unpublish",
    auth=AuthBearer(),
    response=AssetSchemaOut,
)
def unpublish_asset(
    request,
    asset: int,
):
    asset = get_my_id_asset(request, asset)
    asset.visibility = "PRIVATE"
    asset.save()
    return asset


@router.get(
    "/{str:userurl}/{asseturl}",
    response=AssetSchemaOut,
)
def get_asset(
    request,
    userurl: str,
    asseturl: str,
):
    # get_object_or_404 raises the wrong error text
    try:
        asset = Asset.objects.get(url=asseturl, owner__url=userurl)
    except Asset.DoesNotExist:
        raise HttpError(404, "Asset not found.")

    if not user_can_view_asset(request, asset):
        raise HttpError(404, "Asset not found.")
    return asset


# @router.post("", status_code=202)
# @router.post("/", status_code=202, include_in_schema=False)
# async def upload_new_assets(
#     background_tasks: BackgroundTasks,
#     current_user: User = Depends(get_current_user),
#     files: List[UploadedFile] = File(...),
# ):
#     if len(files) == 0:
#         raise HTTPException(422, "No files provided.")
#     job_snowflake = generate_snowflake()
#     background_tasks.add_task(
#         upload_background, current_user, files, None, job_snowflake
#     )
#     return {"upload_job": str(job_snowflake)}


@router.get(
    "",
    response=List[AssetSchemaOut],
)
@router.get(
    "/",
    response=List[AssetSchemaOut],
    include_in_schema=False,
)
@paginate
def get_assets(
    request,
    curated: bool = False,
    name: Optional[str] = None,
    description: Optional[str] = None,
    ownername: Optional[str] = None,
    format: Optional[str] = None,
    filters: AssetFilters = Query(...),
):
    # TODO(james): limit max pagination to 100 results
    # TODO(james): `limit` query param should be `pageSize`; need to find out
    # what `offset` should be
    q = Q(visibility=PUBLIC)

    if filters.tag:
        tags = Tag.objects.filter(name__in=filters.tag)
        q &= Q(tags__in=tags)
    if curated:
        q &= Q(curated=True)
    if name:
        q &= Q(name__icontains=name)
    if description:
        q &= Q(description__icontains=description)
    if ownername:
        q &= Q(owner__displayname__icontains=ownername)
    if format:
        q &= Q(formats__contains=[{"format": format}])
    assets = Asset.objects.filter(q).distinct()

    return assets

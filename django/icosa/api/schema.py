from datetime import datetime
from typing import List, Literal, Optional

from icosa.models import Asset
from ninja import Field, ModelSchema, Schema
from pydantic import EmailStr


class LoginToken(Schema):
    access_token: str
    token_type: str


class DeviceCodeSchema(Schema):
    deviceCode: str


class NewUser(Schema):
    email: EmailStr
    url: Optional[str] = None
    password: str
    displayName: str


class FullUserSchema(Schema):
    id: int
    url: str
    email: EmailStr
    displayname: str
    description: str


class UserSchema(Schema):
    url: str
    displayname: str
    description: Optional[str]


class PatchUserSchema(Schema):
    url: Optional[str] = None
    displayname: Optional[str] = None
    description: Optional[str] = None


class PasswordReset(Schema):
    email: str


class PasswordChangeToken(Schema):
    token: str
    newPassword: str


class PasswordChangeAuthenticated(Schema):
    oldPassword: str
    newPassword: str


class EmailChangeAuthenticated(Schema):
    newEmail: str
    currentPassword: str


# Poly helpers
class PolyResourceSchema(Schema):
    relativePath: str
    url: str
    contentType: str


class PolyFormatComplexity(Schema):
    triangleCount: Optional[str] = None
    lodHint: Optional[int] = None


class PolyFormat(Schema):
    root: PolyResourceSchema
    resources: Optional[List[PolyResourceSchema]] = None
    formatComplexity: Optional[PolyFormatComplexity] = None
    formatType: str


class PolyQuaternion(Schema):
    x: Optional[float] = None
    y: Optional[float] = None
    z: Optional[float] = None
    w: Optional[float] = None


class PolyPresentationParams(Schema):
    orientingRotation: Optional[PolyQuaternion]
    colorSpace: Optional[str] = None
    backgroundColor: Optional[str] = None


class PolyRemixInfo(Schema):
    sourceAsset: List[str]


class PolyPizzaCreator(Schema):
    Username: str
    DPURL: str


class PolyPizzaOrbit(Schema):
    phi: str
    radius: str
    theta: str


class PolyPizzaAsset(Schema):
    ID: str
    Title: str
    Creator: Optional[PolyPizzaCreator]
    Description: Optional[str]
    Tags: List[str]
    # Uploaded: Optional[str]
    Thumbnail: Optional[str]
    Licence: Optional[str]
    Attribution: str
    Download: str
    # TriCount: int
    Category: str
    Animated: bool
    Orbit: Optional[PolyPizzaOrbit]


class PolyAsset(Schema):
    name: str
    displayName: str
    authorName: str
    description: Optional[str] = None
    createTime: str
    updateTime: str
    formats: List[PolyFormat]
    thumbnail: Optional[PolyResourceSchema] = None
    licence: Optional[str] = None
    visibility: str
    isCurated: Optional[bool] = None
    presentationParams: Optional[PolyPresentationParams]
    metadata: Optional[str] = None
    remixInfo: Optional[PolyRemixInfo] = None


class PolyPizzaList(Schema):
    results: List[PolyPizzaAsset]


class PolyList(Schema):
    assets: List[PolyAsset]
    nextPageToken: str
    totalSize: int


# Asset data
class SubAssetFormat(Schema):
    id: int  # TODO(james) should output a str
    url: str
    format: str


class AssetResource(Schema):
    relativePath: str
    contentType: str
    url: str

    @staticmethod
    def resolve_relativePath(obj):
        return obj.relative_path

    @staticmethod
    def resolve_contentType(obj):
        if obj.contenttype:
            return obj.contenttype
        else:
            return ""

    @staticmethod
    def resolve_url(obj):
        return obj.url


class Thumbnail(Schema):
    relativePath: Optional[str] = None
    contentType: Optional[str] = None
    url: Optional[str] = None


class FormatComplexity(Schema):
    triangleCount: Optional[int] = None
    lodHint: Optional[int] = None

    @staticmethod
    def resolve_triangleCount(obj):
        return obj.triangle_count

    @staticmethod
    def resolve_lodHint(obj):
        return obj.lod_hint


class AssetFormat(Schema):
    root: AssetResource
    resources: List[AssetResource]
    formatComplexity: FormatComplexity
    formatType: str
    # remix info

    @staticmethod
    def resolve_root(obj):
        return obj.polyresource_set.filter(is_root=True).first()

    @staticmethod
    def resolve_resources(obj):
        return obj.polyresource_set.filter(is_root=False)

    @staticmethod
    def resolve_formatType(obj):
        return obj.format_type

    @staticmethod
    def resolve_formatComplexity(obj):
        return obj.formatcomplexity_set.first()


class AssetFilters(Schema):
    category: Optional[str] = None
    curated: bool = False
    format: Optional[str] = None
    keywords: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    authorName: Optional[str] = None
    author_name: Optional[str] = None
    tag: List[str] = Field(None, alias="tag")
    orderBy: Optional[str] = None
    order_by: Optional[str] = None


class _DBAsset(ModelSchema):
    name: str
    description: Optional[str]
    authorId: str
    createTime: datetime = Field(..., alias=("create_time"))
    updateTime: datetime = Field(..., alias=("update_time"))
    url: Optional[str]
    formats: List[AssetFormat]
    displayName: str = Field(..., alias=("name"))
    visibility: str
    tags: List[str] = []
    isCurated: Optional[bool] = Field(None, alias=("curated"))
    thumbnail: Optional[Thumbnail]
    ownerurl: str = Field(None, alias=("owner.url"))
    authorName: str
    presentationParams: Optional[PolyPresentationParams] = None

    class Config:
        model = Asset
        model_fields = ["url"]

    @staticmethod
    def resolve_formats(obj, context):
        return [f for f in obj.polyformat_set.all()]

    @staticmethod
    def resolve_tags(obj):
        return [t.name for t in obj.tags.all()]

    @staticmethod
    def resolve_thumbnail(obj):
        data = {}
        if obj.thumbnail:
            data = {
                "relativePath": obj.thumbnail.name.split("/")[-1],
                "contentType": obj.thumbnail_contenttype,
                "url": obj.thumbnail.url,
            }
        return data

    @staticmethod
    def resolve_authorId(obj):
        if not obj.owner:
            return ""
        else:
            return str(obj.owner.id)

    @staticmethod
    def resolve_authorName(obj):
        if obj.owner:
            return f"{obj.owner}"
        else:
            return ""

    @staticmethod
    def resolve_presentationParams(obj):
        params = {}
        params["backgroundColor"] = obj.background_color
        params["orientingRotation"] = {
            "x": getattr(obj, "orienting_rotation_x", None),
            "y": getattr(obj, "orienting_rotation_y", None),
            "z": getattr(obj, "orienting_rotation_z", None),
            "w": getattr(obj, "orienting_rotation_w", None),
        }
        params["colorSpace"] = obj.color_space
        return params


class AssetSchemaIn(_DBAsset):
    pass


class AssetSchemaOut(_DBAsset):
    # TODO: If this doesn't differ from AssetSchemaIn, we should probably
    # remove inheritence.
    pass


class AssetPatchData(Schema):
    name: Optional[str]
    url: Optional[str]
    description: Optional[str]
    visibility: Optional[str]


class UploadJobSchemaOut(Schema):
    upload_job: int
    edit_url: str


class OembedOut(Schema):
    type: Literal["rich"]
    version: Literal["1.0"]
    title: Optional[str] = None  # A text title, describing the resource.
    author_name: Optional[str] = (
        None  # The name of the author/owner of the resource.
    )
    author_url: Optional[str] = (
        None  # A URL for the author/owner of the resource.
    )
    provider_name: Optional[str] = None  # The name of the resource provider.
    provider_url: Optional[str] = None  # The url of the resource provider.
    cache_age: Optional[str] = (
        None  # The suggested cache lifetime for this resource, in seconds. Consumers may choose to use this value or not.
    )
    thumbnail_url: Optional[str] = (
        None  # A URL to a thumbnail image representing the resource. The thumbnail must respect any maxwidth and maxheight parameters. If this parameter is present, thumbnail_width and thumbnail_height must also be present.
    )
    thumbnail_width: Optional[str] = (
        None  # The width of the optional thumbnail. If this parameter is present, thumbnail_url and thumbnail_height must also be present.
    )
    thumbnail_height: Optional[str] = (
        None  # The height of the optional thumbnail. If this parameter is present, thumbnail_url and thumbnail_width must also be present.
    )
    # Specific to "rich" type
    html: str
    width: int
    height: int

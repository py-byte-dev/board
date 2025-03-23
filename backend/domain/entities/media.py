from dataclasses import dataclass
from enum import StrEnum
from io import BytesIO


class MediaType(StrEnum):
    PNG = 'png'
    GIF = 'mp4'


class StoreMediaName(StrEnum):
    PC_PREVIEW = 'pc-preview'
    MOBILE_PREVIEW = 'mobile-preview'
    PC_MAIN = 'pc-main'
    MOBILE_MAIN = 'mobile-main'


class BannerMediaName(StrEnum):
    PC = 'pc-banner'
    MOBILE = 'mobile-banner'


@dataclass(slots=True)
class Media:
    media_obj: BytesIO
    extension: MediaType

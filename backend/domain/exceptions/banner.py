from backend.domain.exceptions.base import BaseDomainError


class BannerNotFoundByIdError(BaseDomainError):
    def __init__(self):
        super().__init__('Banner not found')


class BannersNotFoundError(BaseDomainError):
    def __init__(self):
        super().__init__('Banners not found')

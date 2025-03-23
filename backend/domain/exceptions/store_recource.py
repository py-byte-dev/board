from backend.domain.exceptions.base import BaseDomainError


class StoreResourceNotFoundById(BaseDomainError):
    def __init__(self):
        super().__init__('Store resource not found')


class StoreResourcesNotFoundError(BaseDomainError):
    def __init__(self):
        super().__init__('Store resources not found')

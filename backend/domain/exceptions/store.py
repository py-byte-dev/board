from backend.domain.exceptions.base import BaseDomainError


class StoreNotFoundByIdError(BaseDomainError):
    def __init__(self):
        super().__init__('Store not found')


class StoresNotFoundError(BaseDomainError):
    def __init__(self):
        super().__init__('Stores not found')


class StoresNotFoundByFiltersError(BaseDomainError):
    def __init__(self):
        super().__init__('Stores not found by filters')

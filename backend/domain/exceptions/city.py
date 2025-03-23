from backend.domain.exceptions.base import BaseDomainError


class CityNotFoundByIdError(BaseDomainError):
    def __init__(self):
        super().__init__('City not found')


class CitiesNotFoundError(BaseDomainError):
    def __init__(self):
        super().__init__('Cities not found')

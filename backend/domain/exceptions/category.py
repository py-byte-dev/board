from backend.domain.exceptions.base import BaseDomainError


class CategoryNotFoundByIdError(BaseDomainError):
    def __init__(self):
        super().__init__('Category not found')


class CategoriesNotFoundError(BaseDomainError):
    def __init__(self):
        super().__init__('Categories not found')

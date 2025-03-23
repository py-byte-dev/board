from backend.domain import exceptions as domain_exceptions
from backend.presentation.api.middlewares import exception_handlers

EXCEPTIONS_MAPPING = {
    domain_exceptions.StoreNotFoundByIdError: exception_handlers.store_not_found_exception_handler,
    domain_exceptions.StoresNotFoundByFiltersError: exception_handlers.stores_not_found_exception_handler,
    domain_exceptions.BannersNotFoundError: exception_handlers.banners_not_found_exception_handler,
    domain_exceptions.CitiesNotFoundError: exception_handlers.cities_not_found_exception_handler,
    domain_exceptions.CategoriesNotFoundError: exception_handlers.categories_not_found_exception_handler,
}

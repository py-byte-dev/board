from uuid import uuid4

from dishka import Provider, Scope, from_context, provide

from backend.application import interfaces
from backend.application.services.pagination import PaginationService
from backend.application.use_cases.banner import (
    DeleteBannerInteractor,
    GetBannerInteractor,
    GetBannersInteractor,
    SaveBannerInteractor,
    UpdateBannerUrlInteractor,
    UpdatePcBannerInteractor,
    UpdateMobileBannerInteractor,
    UpdateBannerDisplayPriorityInteractor
)
from backend.application.use_cases.category import (
    DeleteCategoryInteractor,
    GetAllCategoriesInteractor,
    GetCategoryInteractor,
    GetStoreCategoriesInteractor,
    SaveCategoriesInteractor,
)
from backend.application.use_cases.city import (
    DeleteCityInteractor,
    GetAllCitiesInteractor,
    GetCityInteractor,
    GetStoreCitiesInteractor,
    SaveCitiesInteractor,
)
from backend.application.use_cases.store import (
    CanAddStoreInteractor,
    DeleteStoreInteractor,
    GetAllStoresInteractor,
    GetStoreDetailsInteractor,
    GetStoreInteractor,
    GetStoresByFilterInteractor,
    SaveStoreInteractor,
    UpdateStoreDescriptionInteractor,
    UpdateStoreDisplayPriorityInteractor,
    UpdateStoreMainMediaMobileInteractor,
    UpdateStoreMainMediaPcInteractor,
    UpdateStoreMainPageUrlInteractor,
    UpdateStorePrevieMediaMobileInteractor,
    UpdateStorePrevieMediaPcInteractor,
    UpdateStoreTitleInteractor,
)
from backend.application.use_cases.store_category import (
    AddStoreCategoryInteractor,
    DeleteStoreCategoryInteractor,
)
from backend.application.use_cases.store_city import (
    AddStoreCityInteractor,
    DeleteStoreCityInteractor,
)
from backend.application.use_cases.store_resource import (
    AddStoreResourcesInteractor,
    DeleteStoreResourceInteractor,
    GetStoreResourcesInteractor,
)
from backend.config import Config


class ApplicationProvider(Provider):
    config = from_context(provides=Config, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def get_uuid_generator(self) -> interfaces.UUIDGenerator:
        return uuid4

    get_city_interactor = provide(GetCityInteractor, scope=Scope.REQUEST)
    get_all_cities_interactor = provide(GetAllCitiesInteractor, scope=Scope.REQUEST)
    get_store_cities_interactor = provide(GetStoreCitiesInteractor, scope=Scope.REQUEST)
    save_cities_interactor = provide(SaveCitiesInteractor, scope=Scope.REQUEST)
    delete_city_interactor = provide(DeleteCityInteractor, scope=Scope.REQUEST)

    get_category_interactor = provide(GetCategoryInteractor, scope=Scope.REQUEST)
    get_all_categories_interactor = provide(GetAllCategoriesInteractor, scope=Scope.REQUEST)
    get_store_categories_interactor = provide(GetStoreCategoriesInteractor, scope=Scope.REQUEST)
    save_category_interactor = provide(SaveCategoriesInteractor, scope=Scope.REQUEST)
    delete_category_interactor = provide(DeleteCategoryInteractor, scope=Scope.REQUEST)

    get_store_interactor = provide(GetStoreInteractor, scope=Scope.REQUEST)
    get_store_details_interactor = provide(GetStoreDetailsInteractor, scope=Scope.REQUEST)
    can_add_store_interactor = provide(CanAddStoreInteractor, scope=Scope.REQUEST)
    get_all_stores_interactor = provide(GetAllStoresInteractor, scope=Scope.REQUEST)
    get_stores_by_filter = provide(GetStoresByFilterInteractor, scope=Scope.REQUEST)
    save_store_interactor = provide(SaveStoreInteractor, scope=Scope.REQUEST)
    update_store_title_interactor = provide(UpdateStoreTitleInteractor, scope=Scope.REQUEST)
    update_store_description_interactor = provide(UpdateStoreDescriptionInteractor, scope=Scope.REQUEST)
    update_store_preview_media_pc_interactor = provide(UpdateStorePrevieMediaPcInteractor, scope=Scope.REQUEST)
    update_store_preview_media_mobile_interactor = provide(UpdateStorePrevieMediaMobileInteractor, scope=Scope.REQUEST)
    update_store_main_media_pc_interactor = provide(UpdateStoreMainMediaPcInteractor, scope=Scope.REQUEST)
    update_store_main_media_mobile_interactor = provide(UpdateStoreMainMediaMobileInteractor, scope=Scope.REQUEST)

    update_store_target_url_interactor = provide(UpdateStoreMainPageUrlInteractor, scope=Scope.REQUEST)
    update_store_priority_interactor = provide(UpdateStoreDisplayPriorityInteractor, scope=Scope.REQUEST)
    delete_store_interactor = provide(DeleteStoreInteractor, scope=Scope.REQUEST)

    add_store_city_interactor = provide(AddStoreCityInteractor, scope=Scope.REQUEST)
    delete_store_city_interactor = provide(DeleteStoreCityInteractor, scope=Scope.REQUEST)

    add_store_category_interactor = provide(AddStoreCategoryInteractor, scope=Scope.REQUEST)
    delete_store_category_interactor = provide(DeleteStoreCategoryInteractor, scope=Scope.REQUEST)

    get_store_resources_interactor = provide(GetStoreResourcesInteractor, scope=Scope.REQUEST)
    delete_store_resource_interactor = provide(DeleteStoreResourceInteractor, scope=Scope.REQUEST)
    add_store_resources_interactor = provide(AddStoreResourcesInteractor, scope=Scope.REQUEST)

    get_banner_interactor = provide(GetBannerInteractor, scope=Scope.REQUEST)
    get_banners_interactor = provide(GetBannersInteractor, scope=Scope.REQUEST)
    save_banner_interactor = provide(SaveBannerInteractor, scope=Scope.REQUEST)
    update_banner_url_interactor = provide(UpdateBannerUrlInteractor, scope=Scope.REQUEST)
    update_banner_display_priority = provide(UpdateBannerDisplayPriorityInteractor, scope=Scope.REQUEST)
    update_pc_banner_interactor = provide(UpdatePcBannerInteractor, scope=Scope.REQUEST)
    update_mobile_banner_interactor = provide(UpdateMobileBannerInteractor, scope=Scope.REQUEST)
    delete_banner_interactor = provide(DeleteBannerInteractor, scope=Scope.REQUEST)

    pagination_service = provide(PaginationService, scope=Scope.REQUEST)

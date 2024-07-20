from app_test.testcases.testcases_api.tc_marketplace_services_config import api_services
import pytest


@pytest.mark.products
@pytest.mark.api
def test_verify_search__1234(envType):
    api_data = api_services.get_eps_service_response("PPR", "products")
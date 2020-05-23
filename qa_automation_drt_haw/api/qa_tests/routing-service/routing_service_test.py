import pytest
import os
from qa_automation_drt_haw.api.api_utils.serviceApi import ServiceAPI, ServiceInfo, Token
from qa_automation_core.api.service import Service
from qa_automation_core.api.api_headers import (get_default_headers,
                                                post_default_headers, post_headers_content_json_accept_text)
from endpoints_routing import endpoints
import json
from qa_automation_drt_haw.settings import Config
from qa_automation_drt_haw.ui.ui_utils.Logs import log

# pytestmark = [pytest.mark.portal, pytest.mark.api_all]

username = Config.portal_2_roles_username
psw = Config.portal_2_roles_password

routing_service_info = ServiceInfo('routing-service')
valid_jwt = Token(username, psw)

service_valid_token = Service(routing_service_info.url, token=str(valid_jwt), sslcert=False)
service_empty_token = Service(routing_service_info.url, token="", sslcert=False)
service_invalid_token = Service(routing_service_info.url, token="9384903hfheh3902hf4893", sslcert=False)


service_expired_token = Service(routing_service_info.url, token="expired", sslcert=False)

@pytest.mark.p0
@pytest.mark.p4
def test_healthcheck_alive():
    """ automation testcase - Verify's that GET /v1/health/alive or API connection alive , when valid JWT cookies token is provided """
    log.info("Testcase Started - Verify's that GET /v1/health/alive or API connection alive , when valid JWT cookies token is provided")
    log.info("Checking Routing service Connection Status")
    res = service_valid_token.get(endpoints.HEALTH_ALIVE, get_default_headers())
    assert res.status_code == 200, "ALIVE status: %s" % res.status_code
    log.info("Routing service connection status: %s", res.status_code)
    log.info("Testcase Ended")

@pytest.mark.p0
@pytest.mark.p4
def test_healthcheck_ready():
    """ automation testcase - Verify's that GET /v1/health/ready or API connection ready , when valid JWT cookies token is provided """
    log.info("Testcase Started - Verify's that GET /v1/health/ready or API connection ready , when valid JWT cookies token is provided")
    log.info("Checking Routing service Connection Ready")
    res = service_valid_token.get(endpoints.HEALTH_READY, get_default_headers())
    assert 200 == res.status_code, "READY status: %s" % res.status_code
    log.info("Routing service connection is ready")
    log.info("Testcase Ended")

@pytest.mark.p0
@pytest.mark.p4
def test_routes_empty_token():
    """ automation testcase - Verify's that GET /v1/routes or API fails with response message - No authorization token provided ,
     when empty token is provided """
    log.info("Testcase Started - Verify's that GET /v1/routes or API fails with response message - No authorization token provided , \
     when empty token is provided")
    log.info("Fetching all routes information using GET request with empty token")
    res = service_empty_token.get(endpoints.ROUTES, get_default_headers())
    assert 401 == res.status_code, "ROUTES status with empty JWT: %s" % res.status_code
    routes = json.loads(res.text_payload)
    log.info("Getting Unauthorized Response")
    assert 'No authorization token provided' == routes['detail']
    assert 'Unauthorized' == routes['title']
    log.info("Testcase Ended")

@pytest.mark.p0
@pytest.mark.p4
def test_routes_invalid_token():
    """ automation testcase - Verify's that GET /v1/routes or API fails with response message - Could not decode token ,
    when invalid token is provided """
    log.info("Testcase Started - Verify's that GET /v1/routes or API fails with response message - Could not decode token , \
    when invalid token is provided")
    log.info("Fetching all routes information using GET request with invalid token")
    res = service_invalid_token.get(endpoints.ROUTES, get_default_headers())
    assert 401 == res.status_code, "ROUTES status with invalid JWT: %s" % res.status_code
    routes = json.loads(res.text_payload)
    log.info("Getting Unauthorized Response")
    assert 'Could not decode token' in routes['detail']
    assert 'Unauthorized' == routes['title']
    log.info("Testcase Ended")

@pytest.mark.p0
@pytest.mark.p4
@pytest.mark.skip(reason='TODO expired_token')
def test_routes_expired_token():
    """ automation testcase - Verify's that GET /v1/routes or API fails with response message - Could not decode token ,
    when expired token is provided """
    log.info("Testcase Started - Verify's that GET /v1/routes or API fails with response message - Could not decode token , \
    when expired token is provided")
    log.info("Fetching all routes information using GET request with expired token")
    res = service_expired_token.get(endpoints.ROUTES, get_default_headers())
    assert 401 == res.status_code, "ROUTES status with invalid JWT: %s" % res.status_code
    log.info("Getting Unauthorized Response")
    assert 'Could not decode token' in res.json_payload['detail']
    assert 'Unauthorized' == res.json_payload['title']
    log.info("Testcase Ended")

@pytest.mark.p0
@pytest.mark.p4
def test_routes_valid_jwt():
    """ automation testcase - Verify's that GET /v1/routes or API fetches routes details ,
    when valid JWT token is provided """
    log.info("Testcase Started - Verify's that GET /v1/routes or API fetches routes details , \
    when valid JWT token is provided")
    log.info("Fetching all routes information using GET request with valid token")
    res = service_valid_token.get(endpoints.ROUTES, get_default_headers())
    assert 200 == res.status_code, "READY status: %s" % res.status_code
    log.info("Fetched all routes information using GET request with valid token")
    log.info("Testcase Ended")

@pytest.mark.p0
@pytest.mark.p4
def test_no_roles():
    """ automation testcase - Verify's that GET /v1/routes or API fetches routes details with no roles in response,
        when valid JWT token is provided """
    log.info("Testcase Started - Verify's that GET /v1/routes or API fetches routes details with no roles in response, \
        when valid JWT token is provided")
    username = Config.portal_no_roles_username
    psw = Config.portal_no_roles_password
    jwt = Token(username, psw)
    log.info("Fetching no routes information using GET request with valid token")
    res = Service(routing_service_info.url, token=str(jwt), sslcert=False).get(endpoints.ROUTES, get_default_headers())

    assert 200 == res.status_code, "ROUTES status: %s" % res.status_code
    assert len(res.json_payload) == 0, "No roles expected: %s" % res.json_payload
    log.info("Fetched no routes information using GET request with valid token")
    log.info("Testcase Ended")

#TODO - user with specified role is required with constant roles for users ("user_with_2_roles", "portal_2_roles")'
test_data = [ ("user_only_chronicle", "portal_chronicle"),
             ("user_no_roles", "portal_no_roles")]
@pytest.mark.p0
@pytest.mark.p4
@pytest.mark.parametrize("test_name, patient", test_data)
def test_routes_verify_services(test_name, patient):
    """ automation testcase - Verify's that GET /v1/routes or API fetches routes details for patient user provide as params
    and verify its service from fixtures data,when valid JWT token is provided """
    log.info("Testcase Started - Verify's that GET /v1/routes or API fetches routes details for patient user provide as params \
    and verify its service from fixtures data,when valid JWT token is provided")
    user = getattr(Config, patient + '_username') #pytest.data.get_user(patient)['username']
    password = getattr(Config, patient + '_password') #decrypt(pytest.data.get_user(patient)['password'], pytest.envpassword)
    roles = pytest.data.get_user(patient)['roles']
    expected_user_services = [x['service_name'] for x in roles]

    jwt = Token(user, password)
    log.info("Fetching all routes/roles information using GET request with valid token")
    service = Service(routing_service_info.url, token=str(jwt), sslcert=False).get(endpoints.ROUTES, get_default_headers())
    assert 200 == service.status_code

    actual_services = service.json_payload
    log.info("Fetching all routes/roles information using GET request with valid token")
    log.info("Validating roles as expected and actual results")
    actual_services = [r['name'] for r in actual_services]
    assert sorted(expected_user_services) == sorted(actual_services), "Services for %s have not matched:\n Expected: %s \n Actual:%s" % (test_name, expected_user_services, actual_services)
    log.info("Validated roles as expected and actual results")
    log.info("Testcase Ended")

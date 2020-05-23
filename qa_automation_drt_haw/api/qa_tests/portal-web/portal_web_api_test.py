import pytest


from qa_automation_drt_haw.api.api_utils.serviceApi import ServiceAPI, ServiceInfo, Token
from qa_automation_core.api.service import Service
from qa_automation_core.api.api_headers import (get_default_headers,
                                                post_default_headers, post_headers_content_json_accept_text)
from endpoints_portal import endpoints
import json
from qa_automation_drt_haw.settings import Config
from qa_automation_drt_haw.ui.ui_utils.Logs import log

username = Config.portal_2_roles_username
psw = Config.portal_2_roles_password
portal_info = ServiceInfo('portal-web')
valid_jwt = Token(username, psw)


portal_web_service_invalid_token = Service(portal_info.url, token=str("8594389jijfi49"), sslcert=False)
portal_web_service_expired_token = Service(portal_info.url, token=str("8594389jijfi49"), sslcert=False)
portal_web_service_empty_token = Service(portal_info.url, token="", sslcert=False)

portal_web_service_valid_token = Service(portal_info.url, jwt_cookie=str(valid_jwt), sslcert=False)

@pytest.mark.p0
@pytest.mark.p4
def test_healthcheck_alive():
    """ automation testcase - Verify's that GET /alive or API connection alive , when valid JWT cookies token is provided """
    log.info("Testcase Started - Verify's that GET /alive or API connection alive , when valid JWT cookies token is provided")
    log.info("Checking Portal web Connection Status")
    res = portal_web_service_valid_token.get(endpoints.HEALTH_ALIVE, get_default_headers())
    assert 200 == res.status_code, "ALIVE status: %s" % res
    log.info("Portal web connection status: %s", res.status_code)
    log.info("Testcase Ended")

@pytest.mark.p0
@pytest.mark.p4
def test_healthcheck_ready():
    """ automation testcase - Verify's that GET /v1/health/ready or API connection ready , when valid JWT cookies token is provided """
    log.info("Testcase Started - Verify's that GET /v1/health/ready or API connection ready , when valid JWT cookies token is provided")
    log.info("Checking Portal web Connection Ready")
    res = portal_web_service_valid_token.get(endpoints.HEALTH_READY, get_default_headers())
    assert 200 == res.status_code, "READY status: %s" % res
    log.info("Portal web connection is ready")
    log.info("Testcase Ended")

@pytest.mark.p0
@pytest.mark.p4
def test_routes_valid_token():
    """ automation testcase - Verify's that GET /api/v1/routes or API fetches all routes information , when valid JWT cookies token is
    provided """
    log.info("Testcase Started - Verify's that GET /api/v1/routes or API fetches all routes information , when valid JWT cookies token is \
    provided")
    log.info("Fetching details of the roles/routes provide to the user")
    res = portal_web_service_valid_token.get(endpoints.ROUTES, get_default_headers())
    assert 200 == res.status_code, "ROUTES status: %s" % res
    log.info("Fetched details of the roles/routes provide to the user")
    log.info("Testcase Ended")

@pytest.mark.p0
@pytest.mark.skip(reason='TODO - user with specified role is required with constant roles')
@pytest.mark.p4
def test_routes_verify_roles():
    """ automation testcase - Verify's that GET /api/v1/routes or API fetches all routes information to validate a role with fixture data ,
    when valid JWT cookies token is provided """
    log.info("Testcase Started - Verify's that GET /api/v1/routes or API fetches all routes information to validate a role with fixture data , \
    when valid JWT cookies token is provided")
    log.info("Fetching details of the roles/routes provide to the user")
    res = portal_web_service_valid_token.get(endpoints.ROUTES, get_default_headers())
    assert 200 == res.status_code, "ROUTES status: %s" % res
    log.info("Fetched details of the roles/routes provide to the user")

    roles = json.loads(res.text_payload)
    expected_roles = ['Biomarker Testing Insights', 'Cohort Builder', 'Molecular Tumor Board Manager',
                      'Patient Data Entry', 'Patient Finder', 'Program Insights']  # todo generate roles auto
    role_name_actual = [r['name'] for r in roles]
    log.info("Validating the roles of the user with expected roles list")
    assert expected_roles == sorted(role_name_actual), "Expected list of roles: %s \n Actial list of roles: %s" %(expected_roles ,sorted(role_name_actual) )
    log.info("Validated the roles of the user with expected roles list successfully")
    log.info("Testcase Ended")

@pytest.mark.p0
@pytest.mark.p4
def test_routes_verify_no_roles():
    """ automation testcase - Verify's that GET /api/v1/routes or API fetches all routes information to validate number of role with fixture data ,
    when valid JWT cookies token is provided """
    log.info("Testcase Started - Verify's that GET /api/v1/routes or API fetches all routes information to validate number of role with fixture data , \
    when valid JWT cookies token is provided")
    username = Config.portal_no_roles_username
    psw = Config.portal_no_roles_password
    log.info("Fetching details of the roles/routes provide to the user with no role")
    res = Service(portal_info.url, jwt_cookie=str(Token(username, psw)), sslcert=False).get(endpoints.ROUTES, get_default_headers())
    assert 200 == res.status_code, "ROUTES status: %s" % res
    log.info("Fetched details of the roles/routes provide to the user with no role")
    roles = json.loads(res.text_payload)
    role_name_actual = [r['name'] for r in roles]
    log.info("Validating user has no roles assigned")
    assert 0 == len(role_name_actual), "No roles expected, %s" % role_name_actual
    log.info("Validated user has no roles assigned")
    log.info("Testcase Ended")


@pytest.mark.p0
@pytest.mark.p4
def test_routes_invalid_token():
    """ automation testcase - Verify's that GET /api/v1/routes or API fetches all routes information to validate number of role with fixture data fails ,
     when invalid JWT cookies token is provided """
    pytest.log_link = 'https://syapse.atlassian.net/browse/AP-37842'
    log.info("Testcase Started - Verify's that GET /api/v1/routes or API fetches all routes information to validate number of role with fixture data fails , \
     when invalid JWT cookies token is provided")
    log.info("Fetching details of the roles/routes provide to the user with invalid token")
    res = portal_web_service_invalid_token.get(endpoints.ROUTES, get_default_headers())
    assert 403 == res.status_code, "ROUTES status (invalid token): %s" % res
    log.info("Authorization error in response")
    log.info("Testcase Ended")


@pytest.mark.p0
@pytest.mark.p4
@pytest.mark.skip(reason='TODO expired_token')
def test_routes_expired_token():
    """ automation testcase - Verify's that GET /api/v1/routes or API fetches all routes information to validate number of role with fixture data fails ,
         when invalid expired JWT cookies token is provided """
    pytest.log_link = 'https://syapse.atlassian.net/browse/AP-37924'
    log.info("Testcase Started - Verify's that GET /api/v1/routes or API fetches all routes information to validate number of role with fixture data fails , \
         when invalid expired JWT cookies token is provided")
    log.info("Fetching details of the roles/routes provide to the user with expired token")
    res = portal_web_service_expired_token.get(endpoints.ROUTES, get_default_headers())
    assert 401 == res.status_code, "ROUTES status (expired token): %s" % res
    log.info("Getting Unauthorized Response")
    log.info("Testcase Ended")

@pytest.mark.p0
@pytest.mark.p4
@pytest.mark.skip(reason='flaky')
def test_routes_empty_token():
    """ automation testcase - Verify's that GET /api/v1/routes or API fetches all routes information to validate number of role with fixture data fails ,
         when JWT cookies token is empty """
    log.info("Testcase Started - Verify's that GET /api/v1/routes or API fetches all routes information to validate number of role with fixture data fails , \
         when JWT cookies token is empty")
    log.info("Fetching details of the roles/routes provide to the user with empty token")
    res = portal_web_service_empty_token.get(endpoints.ROUTES, get_default_headers())
    assert 401 == res.status_code, "ROUTES status (empty token): %s" % res
    log.info("Getting Unauthorized Response")
    log.info("Testcase Ended")


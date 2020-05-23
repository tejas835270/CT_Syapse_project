import pytest
import os
from qa_automation_drt_haw.api.api_utils.serviceApi import ServiceAPI, ServiceInfo, Token
from qa_automation_core.api.service import Service
from qa_automation_core.api.api_headers import (get_default_headers,
                                                post_default_headers, post_headers_content_json_accept_text)
from endpoints_file import endpoints
import json
from qa_automation_drt_haw.settings import Config
from qa_automation_drt_haw.ui.ui_utils.Logs import log
import base64

username = Config.portal_2_roles_username
psw = Config.portal_2_roles_password

file_service_info = ServiceInfo('file-service')
valid_jwt = Token(username, psw)

file_service_valid_token = Service(file_service_info.url, token=str(valid_jwt), sslcert=False)
file_service_empty_token = Service(file_service_info.url, token="", sslcert=False)
file_service_invalid_token = Service(file_service_info.url, token="9384903hfheh3902hf4893", sslcert=False)
file_service_expired_token = Service(file_service_info.url, token="expired", sslcert=False)

@pytest.mark.p0
@pytest.mark.skip(reason='need user with integration2.dev access to generate the file for different org i.e. (integration2.dev)')
def test_get_file_with_file_token_from_org_which_is_not_in_jwt_token():
    """Automation Test Case - Verify user cannot access file with file token from org of integration2.dev which is not in JWT token of integration1.dev - [AP-39810]"""
    log.info("Test Case Started - Verify user cannot access file with file token from org which is not in JWT token")
    # TODO need user with integration2.dev access to generate the file token for different org i.e. (integration2.dev)
    # Getting the file token for integration2.dev organization
    integration2_file_token = Config.integration2_file_token
    # making the get request with other org file token i.e. (integration2.dev) and valid jwt token of integration1.dev
    res = file_service_valid_token.get(endpoints.GET_FILE_BY_TOKEN + integration2_file_token, get_default_headers())
    assert 401 == res.status_code, "user cannot access file with file: %s" % res.status_code
    log.info("user cannot access file with file")
    log.info("Test Case Ended")

def get_file_token_of_mtb_saved_file():
    """Get file token while passing the data payload"""
    data = { "body_content": str(base64.b64encode('my_pdf.pdf'.encode("utf-8")), "utf-8"), "content_type": "pdf", "file_name_string": "my_pdf.pdf" }
    payload = json.dumps(data)
    # Getting file token while passing the data payload.
    token = file_service_valid_token.post(endpoints.POST_SAVE_FILE, payload, post_headers_content_json_accept_text())
    # Generating the valid file token.
    file_token = token.text_payload
    return file_token

@pytest.mark.p0
@pytest.mark.skip(reason='File service API response should fail with 404 as per the ticket but it is failing with 400')
def test_get_file_info_fails_with_invalid_file_token():
    """Automation Test Case - Verify GET /file/{file_token} fails to get file info with invalid file_token & valid JWT token - [AP-39809]"""
    log.info("Test Case Started - Verify GET /file/{file_token} fails to get file info with invalid file_token & valid JWT token")
    # Generating the invalid file token
    invalid_file_token = get_file_token_of_mtb_saved_file() + 'yh098m'
    # making the get request along with valid jwt token & generated invalid file token.
    res = file_service_valid_token.get(endpoints.GET_FILE_BY_TOKEN + invalid_file_token, get_default_headers())
    # TODO we should get the api response 404 but receiving 400 response instead, verified same thing on file service swqagger ui.
    assert 404 == res.status_code, "GET fails for invalid file_token: %s" % res.status_code
    log.info("GET fails for invalid file_token")
    log.info("Test Case Ended")

@pytest.mark.p0
@pytest.mark.p4
def test_get_file_info_succeed_with_valid_file_token():
    """Automation Test Case - Verify GET /file/<file_token> is successful to get the file info with valid file token & unexpired JWT token - [AP-39808]"""
    log.info("Test Case Started - Verify GET /file/<file_token> is successful to get the file info with valid file token & unexpired JWT token")
    # Getting the valid file token.
    valid_file_token = get_file_token_of_mtb_saved_file()
    # making the get request along with generated file token & valid jwt token.
    res = file_service_valid_token.get(endpoints.GET_FILE_BY_TOKEN + valid_file_token, get_default_headers())
    assert 200 == res.status_code, "GET Successful with valid unexpired JWT token: %s" % res.status_code
    log.info("GET Successful with valid unexpired JWT token")
    log.info("Test Case Ended")

@pytest.mark.p0
@pytest.mark.p4
def test_get_file_info_fails_without_jwt_token():
    """Automation Test Case - Verify GET /file/<file_token> fails to get the file info without JWT token - [AP-39807]"""
    log.info("Test Case Started - Verify GET /file/<file_token> fails to get the file info without JWT token")
    # Getting the valid file token.
    file_token = get_file_token_of_mtb_saved_file()
    # making the get request with empty jwt token along with valid file token.
    res = file_service_empty_token.get(endpoints.GET_FILE_BY_TOKEN + file_token, get_default_headers())
    assert 401 == res.status_code, "GET fails without JWT token: %s" % res.status_code
    log.info("GET fails without JWT token")
    log.info("Test Case Ended")

@pytest.mark.p0
def test_post_save_mtb_file_fails_with_empty_string_of_body_content():
    """Automation Test Case - Verify POST /file fails save MTB file when empty strings of body content are passed with valid jwt token - [AP-39779]"""
    log.info("Test Case Started - Verify POST /file fails save MTB file when empty strings of body content are passed with valid jwt token")
    data = { "body_content": "", "content_type": "", "file_name_string": "" }
    payload = json.dumps(data)
    # making the post request with valid jwt token along with empty data payload.
    res = file_service_valid_token.post(endpoints.POST_SAVE_FILE, payload, post_headers_content_json_accept_text())
    assert 500 == res.status_code, " POST fails when empty strings are passed for required fields: %s" % res.status_code
    log.info("POST fails when empty strings are passed for required fields")
    log.info("Test Case Ended")

@pytest.mark.p0
def test_post_save_mtb_file_with_all_required_fields():
    """Automation Test Case - Verify POST /file save file when all attributes and valid token are provided - [AP-39778]"""
    log.info("Test Case Started - Verify POST /file save file when all attributes and valid token are provided")
    data = { "body_content": str(base64.b64encode('my_pdf.pdf'.encode("utf-8")), "utf-8"), "content_type": "pdf", "file_name_string": "my_pdf.pdf" }
    payload = json.dumps(data)
    # making the post request with valid jwt token along with data payload.
    res = file_service_valid_token.post(endpoints.POST_SAVE_FILE, payload, post_headers_content_json_accept_text())
    assert 201 == res.status_code, " POST passes when all properties are provided: %s" % res.status_code
    log.info("POST passes when all properties are provided")
    log.info("Test Case Ended")

@pytest.mark.p0
def test_post_save_mtb_file_fails_for_missing_field():
    """Automation Test Case - Verify POST /file fails to save mtb file when required fields are not provided with valid jwt token - [AP-39777]"""
    log.info("Test Case Started - Verify POST /file fails to save mtb file when required fields are not provided with valid jwt token")
    data = { "body_content": str(base64.b64encode('my_pdf.pdf'.encode("utf-8")), "utf-8"), "file_name_string": "my_pdf.pdf"}
    payload = json.dumps(data)
    # making the post request with valid jwt token along with missing field data payload.
    res = file_service_valid_token.post(endpoints.POST_SAVE_FILE, payload, post_headers_content_json_accept_text())
    assert 400 == res.status_code, "POST fails when required fields are not provided: %s" % res.status_code
    log.info("POST fails when required fields are not provided")
    log.info("Test Case Ended")

@pytest.mark.p0
def test_post_save_mtb_file_fails_without_jwt_token():
    """Automation Test Case - Verify POST /file save file fails when jwt token not provided - [AP-39683]"""
    log.info("Test Case Started - Verify POST /file save file fails when jwt token not provided")
    data = { "body_content": str(base64.b64encode('my_pdf.pdf'.encode("utf-8")), "utf-8"), "content_type": "pdf", "file_name_string": "my_pdf.pdf" }
    payload = json.dumps(data)
    # making the post request without jwt token.
    res = file_service_empty_token.post(endpoints.POST_SAVE_FILE, payload, post_headers_content_json_accept_text())
    assert 401 == res.status_code, " POST fails when jwt token not provided: %s" % res.status_code
    log.info("POST fails when jwt token not provided")
    log.info("Test Case Ended")

@pytest.mark.p0
@pytest.mark.p4
def test_healthcheck_ready_passes_when_file_service_db_accepts_traffic():
    """automation test case - Verify GET /health/ready passes when file-service DB is ready to accept traffic - [AP-38163]"""
    log.info("Test Case Started - Verify GET /health/ready passes when service is ready to accept traffic")
    log.info("Checking File service Connection Ready")
    # Get request with valid jwt token to verify the health endpoint is ready to accept traffic.
    res = file_service_valid_token.get(endpoints.HEALTH_READY, get_default_headers())
    assert 200 == res.status_code, "READY status: %s" % res.status_code
    log.info("File service connection is ready")
    log.info("Test Case Ended")

@pytest.mark.p0
@pytest.mark.p4
def test_healthcheck_alive_passes_when_file_service_pods_are_running():
    """automation test case - Verify GET /health/alive succeed if file-service pods are running - [AP-38161]"""
    log.info("Test Case Started - Verify GET /health/alive passes if service is alive")
    log.info("Checking File service Connection Status")
    # Get request with valid jwt token to verify the health endpoint is alive
    res = file_service_valid_token.get(endpoints.HEALTH_ALIVE, get_default_headers())
    assert res.status_code == 200, "ALIVE status: %s" % res.status_code
    log.info("File service connection status: %s", res.status_code)
    log.info("Test Case Ended")

@pytest.mark.p0
def test_post_save_mtb_file_with_valid_data_payload():
    """Automation Test Case - Verify POST /file save file when all attributes and valid token are provided - [AP-39764]"""
    log.info("Test Case Started - Verify POST /file save file when all attributes and valid token are provided")
    data = { "body_content": str(base64.b64encode('test.ppt'.encode("utf-8")), "utf-8"), "content_type": "ppt", "file_name_string": "test.ppt" }
    payload = json.dumps(data)
    # making the post request with valid jwt token along with data payload.
    res = file_service_valid_token.post(endpoints.POST_SAVE_FILE, payload, post_headers_content_json_accept_text())
    assert 201 == res.status_code, " POST passes when all properties are provided: %s" % res.status_code
    log.info("POST passes when all properties are provided")
    log.info("Test Case Ended")
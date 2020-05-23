from datetime import datetime
from qa_automation_drt_haw.settings import Config
import pytest
from qa_automation_drt_haw.api.api_utils.serviceApi import ServiceAPI, ServiceInfo, Token
from qa_automation_core.api.service import Service
from qa_automation_core.api.api_headers import (get_default_headers,
                                                post_default_headers, post_headers_content_json_accept_text)
from endpoints_flatstore import endpoints
from qa_automation_drt_haw.ui.ui_utils.Logs import log
from qa_automation_drt_haw.api.qa_test_data.data_generator import Data_Generator
import string

"""Data_Generator Class -Generating string for patients search and string patient information to use in testcase methods"""
patient_id = Data_Generator('pre-population').patients_info

username = Config.portal_2_roles_username
psw = Config.portal_2_roles_password

chronicle_patient_info = ServiceInfo('flatstore-patient')
valid_jwt = Token(username, psw)

chronicle_patient_service_valid_token = Service(chronicle_patient_info.url, token=str(valid_jwt), sslcert=False)
chronicle_patient_service_empty_token = Service(chronicle_patient_info.url, token="", sslcert=False)
chronicle_patient_service_invalid_token = Service(chronicle_patient_info.url, token="948390hffh49", sslcert=False)
# TODO
chronicle_patient_service_expired_token = Service(chronicle_patient_info.url, token="expired", sslcert=False)

patient_prepopulation_end_point = endpoints.PATIENT_PREPOPULATION
endpoint_temp = patient_prepopulation_end_point + patient_id

@pytest.mark.p0
@pytest.mark.p4
def test_pre_population_valid_token():
    """ automation testcase - Verify's that GET /v1/patient_prepopulation/{patient_id} or API fetches patient prepopulation details,
     when valid token is provided """
    log.info("Testcase Started - Verify's that GET /v1/patient_prepopulation/{patient_id} or API fetches patient prepopulation details, \
     when valid token is provided")
    log.info("Fetching patients prepopulation details using patientId as parameter with valid token")
    res = chronicle_patient_service_valid_token.get(endpoint_temp, get_default_headers())
    assert 200 == res.status_code, "CHRONICLE PATIENTS:patient_prepopulation  status: %s" % res
    log.info("Fetched patients prepopulation details using patientId as parameter with valid token")
    log.info("Testcase Ended")

@pytest.mark.p0
@pytest.mark.p4
def test_pre_population_empty_token():
    """ automation testcase - Verify's that GET /v1/patient_prepopulation/{patient_id} or API fails to fetches patient prepopulation details,
    when token is not provided """
    log.info("Testcase Started - Verify's that GET /v1/patient_prepopulation/{patient_id} or API fails to fetches patient prepopulation details, \
    when token is not provided")
    log.info("Fetching patients prepopulation details using patientId as parameter with empty token")
    res = chronicle_patient_service_empty_token.get(endpoint_temp, get_default_headers())
    assert 401 == res.status_code, "CHRONICLE PATIENTS:patient_prepopulation  status: %s" % res.status_code
    log.info("Getting Unauthorized Response")
    log.info("Testcase Ended")

@pytest.mark.p0
@pytest.mark.p4
@pytest.mark.skip(reason='TODO expired_token')
def test_pre_population_expired_token():
    """ automation testcase - Verify's that GET /v1/patient_prepopulation/{patient_id} or API fails to fetches patient prepopulation details,
    when expired token is provided """
    log.info("Testcase Started - Verify's that GET /v1/patient_prepopulation/{patient_id} or API fails to fetches patient prepopulation details, \
    when expired token is provided")
    log.info("Fetching patients prepopulation details using patientId as parameter with expired token")
    res = chronicle_patient_service_expired_token.get(endpoint_temp, get_default_headers())
    assert 401 == res.status_code, "CHRONICLE PATIENTS:patient_prepopulation  status: %s" % res.status_code
    log.info("Getting Unauthorized Response")
    log.info("Testcase Ended")

@pytest.mark.p0
@pytest.mark.p4
def test_pre_population_invalid_token():
    """ automation testcase - Verify's that GET /v1/patient_prepopulation/{patient_id} or API fails to fetches patient prepopulation details,
    when invalid token is provided """
    log.info("Testcase Started - Verify's that GET /v1/patient_prepopulation/{patient_id} or API fails to fetches patient prepopulation details, \
    when invalid token is provided")
    log.info("Fetching patients prepopulation details using patientId as parameter with invalid token")
    res = chronicle_patient_service_invalid_token.get(endpoint_temp, get_default_headers())
    assert 401 == res.status_code, "CHRONICLE PATIENTS:patient_prepopulation  status: %s" % res.status_code
    log.info("Getting Unauthorized Response")
    log.info("Testcase Ended")

@pytest.mark.p0
@pytest.mark.p4
def test_pre_population_empty_id():
    """ automation testcase - Verify's that GET /v1/patient_prepopulation/{patient_id} or API fails to fetches patient prepopulation details,
    when patient_id is not provided """

    log.info("Testcase Started - Verify's that GET /v1/patient_prepopulation/{patient_id} or API fails to fetches patient prepopulation details, \
    when patient_id is not provided")
    log.info("Fetching patients prepopulation details without patientId as parameter")
    res = chronicle_patient_service_valid_token.get(patient_prepopulation_end_point, get_default_headers())
    assert 404 == res.status_code, "CHRONICLE PATIENTS:patient_prepopulation status: %s" % res
    log.info("Getting no result found as response")
    log.info("Testcase Ended")

@pytest.mark.p0
@pytest.mark.p4
def test_pre_population_patient_not_found():
    """ automation testcase - Verify's that GET /v1/patient_prepopulation/{patient_id} or API fails to fetches patient prepopulation details,
    when invalid patient_id is provided """
    log.info("Testcase Started - Verify's that GET /v1/patient_prepopulation/{patient_id} or API fails to fetches patient prepopulation details, \
    when invalid patient_id is provided")
    log.info("Fetching patients prepopulation details with invalid patientId as parameter")
    res = chronicle_patient_service_valid_token.get(patient_prepopulation_end_point+patient_id+"-=-=-", get_default_headers())
    assert 404 == res.status_code, "CHRONICLE PATIENTS:patient_prepopulation status: %s" % res.status_code
    assert "Patient with UUID: %s not found." %(patient_id+"-=-=-") == res.json_payload
    log.info("Getting no result found as response")
    log.info("Testcase Ended")
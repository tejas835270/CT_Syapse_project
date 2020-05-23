import base64

import pytest
from qa_automation_drt_haw.settings import Config
from qa_automation_drt_haw.api.api_utils.serviceApi import ServiceAPI, ServiceInfo, Token
from qa_automation_core.api.service import Service
# from qa_automation_core.api.api_headers import ApiHeaders
from qa_automation_core.api.api_headers import get_default_headers, post_default_headers, \
    post_headers_content_json_accept_text
from endpoints_mtb import endpoints
from qa_automation_drt_haw.ui.ui_utils.Logs import log
import re
import json
import os
import string
from qa_automation_drt_haw.api.qa_test_data.data_generator import Data_Generator

"""Data_Generator Class - Generating string for patients search and string patient information to use in testcase methods"""
patient_info = Data_Generator('mtb').patients_info

username = Config.portal_2_roles_username
psw = Config.portal_2_roles_password
userId = pytest.data.get_user('portal_2_roles')['userId']

mtb_info = ServiceInfo('mtb-web')
minerva_service_info = ServiceInfo('minerva-service')
valid_jwt = Token(username, psw)
exp_timestap = os.popen("date -v+60M +%s").read().split('\n')[0]
cookies_info = {'auth': str(valid_jwt), 'userId': userId, 'exp-timestamp': exp_timestap}

mtb_web_service_empty_token = Service(mtb_info.url, token="", sslcert=False)
mtb_web_service_valid_token = Service(mtb_info.url, jwt_cookie=str(valid_jwt), sslcert=False)
mtb_web_service_valid_cookies = Service(mtb_info.url, jwt_cookie=cookies_info, sslcert=False)
mtb_web_service_invalid_token = Service(mtb_info.url, token="8594389jijfi49", sslcert=False)
mtb_web_service_expired_token = Service(mtb_info.url, token="expired", sslcert=False)

minerva_service_valid_token = Service(minerva_service_info.url, token=str(valid_jwt), sslcert=False)

regex = re.compile('[@_!#$%^&*()<>?/|}{~:]')
xfail = pytest.mark.xfail


@pytest.mark.p0
@pytest.mark.p4
def test_healthcheck_alive():
    """ automation testcase - Verify's that GET /alive or API connection alive , when valid JWT cookies token is provided """
    log.info(
        "Testcase Started - Verify's that GET /alive or API connection alive , when valid JWT cookies token is provided")
    res = mtb_web_service_valid_token.get(endpoints.HEALTH_ALIVE, get_default_headers())
    log.info("Checking MTB Service Connection Status")
    assert '{"alive":true}' == res.text_payload, "ALIVE status: %s" % res.status_code
    log.info("MTB Service connection status: %s", res.text_payload)
    assert 200 == res.status_code, "ALIVE status: %s" % res.status_code
    log.info("Tetscase Ended")


@pytest.mark.p0
@pytest.mark.p4
@xfail
def test_healthcheck_not_alive():
    """ automation testcase - Verify's that GET /alive or API connection alive fails, when service is down and valid JWT cookies token is provided - [AP-37660]"""
    log.info(
        "Testcase Started - Verify's that GET /alive or API connection alive fails, when service is down and valid JWT cookies token is provided")
    res = mtb_web_service_valid_token.get(endpoints.HEALTH_ALIVE, get_default_headers())
    log.info("Checking MTB Service Connection Status")
    assert 503 == res.status_code, "ALIVE status: %s" % res.status_code
    assert "upstream connect error or disconnect/reset before headers. reset reason: connection failure" == res.text_payload, "ALIVE status: %s" % res
    log.info("MTB Service connection status: %s", res.text_payload)
    log.info("Tetscase Ended")


@pytest.mark.p0
@pytest.mark.p4
def test_healthcheck_ready():
    """ automation testcase - Verify's that GET /ready or API connection ready , when valid JWT cookies token is provided - [AP-37662]"""
    log.info(
        "Testcase Started - Verify's that GET /ready or API connection ready , when valid JWT cookies token is provided")
    res = mtb_web_service_valid_token.get(endpoints.HEALTH_READY, get_default_headers())
    log.info("Checking MTB Service Connection Ready")
    assert 200 == res.status_code, "READY status: %s" % res.status_code
    log.info("MTB Service Connection is Ready")
    log.info("Tetscase Ended")


@pytest.mark.p0
@pytest.mark.p4
@xfail
def test_healthcheck_not_ready():
    """ automation testcase - Verify's that GET /ready or API connection ready fails, when service is down and valid JWT cookies token is provided - [AP-37663]"""
    log.info(
        "Testcase Started - Verify's that GET /ready or API connection ready fails, when service is down and valid JWT cookies token is provided")
    res = mtb_web_service_valid_token.get(endpoints.HEALTH_READY, get_default_headers())
    log.info("Checking MTB Service Connection Ready")
    # Checking service is down or not
    assert 503 == res.status_code, "ALIVE status: %s" % res.status_code
    assert "upstream connect error or disconnect/reset before headers. reset reason: connection failure" == res.text_payload, "ALIVE status: %s" % res
    log.info("MTB Service Connection is not Ready")
    log.info("Tetscase Ended")


@pytest.mark.p0
@pytest.mark.skip(reason='404 status code data not found.')
# TODO mtb-web service post case - /api/v1/case is giving a 500 internal server error so hiting a minerva-service endpoint
def test_get_case_by_uuid_with_valid_token():
    """ automation testcase - Verify's that GET /api/v1/case/ successful using uuid value in url , when valid JWT cookies token is provided - [AP-39188]"""
    log.info(
        "Testcase Started - Verify's that GET /api/v1/case/ successful using uuid value in url , when valid JWT cookies token is provided")
    data = {'patientId': patient_info[0]['patientId']}
    log.info("Payload data generated, Patient Id provided")
    payload = json.dumps(data)

    res = minerva_service_valid_token.post(endpoints.POST_CASES, payload,
                                           post_headers_content_json_accept_text())
    log.info("Creating a new case using post request by providing patientId")
    assert 201 == res.status_code, "CASE POST status: %s" % res
    log.info("New Case created successfully")

    casesId = res.text_payload
    log.info("Fetching caseId from newly created case")
    res = mtb_web_service_valid_token.get(endpoints.MTB_GET_CASE_UUID + casesId, get_default_headers())
    log.info("Validating a newly created case with MTB Service case url by providing UUID")
    assert 200 == res.status_code, "GET CASE by UUID status: %s" % res
    log.info("Validated case successfully using UUID")
    log.info("Tetscase Ended")


@pytest.mark.p0
@pytest.mark.p4
@pytest.mark.skip(reason='flaky(same reason given in portal web api test file)')
def test_get_cases_empty_token():
    """ automation testcase - Verify's that GET /api/v1/cases fails without JWT cookies token -[AP-37753]"""
    log.info("Testcase Started - Verify's that GET /api/v1/cases fails without JWT cookies token")
    log.info("Fetching case using GET Request with empty JWT token")
    # Fetching case details with empty token
    res = mtb_web_service_empty_token.get(endpoints.MTB_GET_CASES, get_default_headers())
    assert 401 == res.status_code, "GET CASES status (empty token): %s" % res
    log.info("Getting Unauthorized Response")
    log.info("Tetscase Ended")


@pytest.mark.p0
def test_create_mtb_case_for_patient_id():
    """ automation testcase - Verify's that POST /api/v1/case successful or create a case using patient information, when valid JWT cookies token is provided """
    pytest.log_link = 'https://syapse.atlassian.net/browse/AP-39520'
    log.info(
        "Testcase Started - Verify's that POST /api/v1/case successful or create a case using patient information, when valid JWT cookies token is provided")
    data = {"patientId": patient_info[0]['patientId']}
    log.info("Payload data generated, Patient Id provided")
    payload = json.dumps(data)

    log.info("Creating a new case using post request by providing patientId")
    # Create case using cookies details
    res = mtb_web_service_valid_cookies.post(endpoints.POST_CASES, payload, post_headers_content_json_accept_text())
    assert 201 == res.status_code, "MTB Case status: %s" % res.status_code
    log.info("New Case created successfully")
    log.info("Tetscase Ended")


@pytest.mark.p0
@pytest.mark.p4
def test_get_cases_with_valid_token():
    """ automation testcase - Verify's that GET /api/v1/cases successful or fetch cases information, when valid JWT cookies token is provided - [AP-37751]"""
    log.info(
        "Testcase Started - Verify's that GET /api/v1/cases successful or fetch cases information, when valid JWT cookies token is provided")
    # Get request to fetch all cases information
    res = mtb_web_service_valid_token.get(endpoints.MTB_GET_CASES, get_default_headers())
    assert 200 == res.status_code, "MTB CASES status: %s" % res.status_code
    log.info("Fetched cases successfully")
    log.info("Tetscase Ended")


@pytest.mark.p0
@pytest.mark.p4
@pytest.mark.skip(reason='wrong response with invalid token')
def test_get_cases_with_invalid_token():
    """ automation testcase - Verify's that GET /api/v1/cases fails or unable to fetch cases information, when invalid JWT token is provided - [AP-37749]"""
    log.info(
        "Testcase Started - Verify's that GET /api/v1/cases fails or unable to fetch cases information, when invalid JWT token is provided")
    # Get request to fetch all cases information with invalid token
    res = mtb_web_service_invalid_token.get(endpoints.MTB_GET_CASES, get_default_headers())
    assert 401 == res.status_code, "MTB CASES status: %s" % res.text_payload
    log.info("Unauthorized Error")
    log.info("Tetscase Ended")


@pytest.mark.p0
@pytest.mark.p4
@pytest.mark.skip(reason='wrong response with expired token')
def test_get_cases_with_expired_token():
    """ automation testcase - Verify's that GET /api/v1/cases fails or unable to fetch cases information, when expired JWT  token is provided - [AP-37750]"""
    log.info(
        "Testcase Started - Verify's that GET /api/v1/cases fails or unable to fetch cases information, when expired JWT  token is provided")
    # Get request to fetch all cases information with expired token
    res = mtb_web_service_expired_token.get(endpoints.MTB_GET_CASES, get_default_headers())
    assert 401 == res.status_code, "MTB CASES status: %s" % res.text_payload
    log.info("Unauthorized Error")
    log.info("Tetscase Ended")


def validate_case_for_org(case_ids):
    a = []
    # Get case details using caseId and fetch patientId, Loop on caseIds
    for caseId in case_ids:
        res = mtb_web_service_valid_token.get(endpoints.MTB_GET_CASE_UUID + caseId, get_default_headers())
        if res.status_code == 200:
            patientId = json.loads(res.text_payload)["patientId"]
            if patientId.split(":")[0]:
                # collect patientId and separate organization name string in one array variable
                a.append(patientId.split(":")[0])
    # Check array contains all duplicate value of same organization and its count should 1 after eliminating duplicate value
    caseOrg = len(list(set(a))) == 1
    return caseOrg


@pytest.mark.p0
@pytest.mark.p4
def test_get_cases_with_valid_token_and_not_return_cases_from_different_org():
    """ automation testcase - Verify's that GET /api/v1/cases successful or fetch cases information, when valid JWT cookies token is provided - [AP-37754]"""
    log.info(
        "Testcase Started - Verify's that GET /api/v1/cases successful or fetch cases information, when valid JWT cookies token is provided")
    res = mtb_web_service_valid_token.get(endpoints.MTB_GET_CASES, get_default_headers())
    assert 200 == res.status_code, "MTB CASES status: %s" % res.status_code
    # Get all the list of caseId in one array
    case_Ids = list(map(lambda x: x['caseId'], json.loads(res.text_payload)["items"]))
    # Valid cases belongs to same organization
    caseValidated = validate_case_for_org(case_Ids)
    assert caseValidated == True, "MTB CASES status: %s" % res.text_payload

    log.info("Tetscase Ended")


@pytest.mark.p0
@pytest.mark.p4
def test_get_case_by_uuid_with_non_existing_uuid():
    """ automation testcase - Verify's that GET /api/v1/case/ fails using invalid uuid value in url , when valid JWT cookies token is provided - [AP-39195]"""
    log.info(
        "Testcase Started - Verify's that GET /api/v1/case/ fails using invalid uuid value in url , when valid JWT cookies token is provided")

    casesId = "99999999-9999-9999-9999-999999999999"  # Invalid caseId or uuid
    log.info("Get case request using non existing or invalid caseId ")
    # Get request to get case details using invalid caseId
    res = mtb_web_service_valid_token.get(endpoints.MTB_GET_CASE_UUID + casesId, get_default_headers())
    assert 404 == res.status_code, "GET CASE by UUID status: %s" % res
    log.info("Case not found response ")
    log.info("Tetscase Ended")


@pytest.mark.p0
@pytest.mark.p4
@pytest.mark.skip(reason='wrong response with no parameter provides 400 bad request error')
def test_get_patients_with_no_parameters():
    """ automation testcase - Verify's that GET /api/v1/patients/ returns no patients, when no parameters are provided and valid JWT cookies token is provided - [AP-39427]"""
    log.info(
        "Testcase Started - Verify's that GET /api/v1/patients/ returns no patients, when no parameters are provided valid JWT cookies token is provided")

    log.info("Get patients request without parameter ")
    # Get request to fetch patients detail without parameter
    res = mtb_web_service_valid_token.get(endpoints.GET_MTB_PATIENTS, get_default_headers())
    assert 200 == res.status_code, "GET Patients status: %s" % res
    log.info("Patients not found response ")
    log.info("Tetscase Ended")


test_data = [patient_info[0]['humanNameFirst'], patient_info[0]['humanNameLast'], patient_info[0]['mrn']]


@pytest.mark.p0
@pytest.mark.p4
@pytest.mark.parametrize("search_by", test_data)
def test_get_patients_multiple_parameter_values(search_by):
    """ automation testcase - Verify's that GET /api/v1/patients/ returns patients information successfully, when search string parameters are provided and valid JWT cookies token is provided - [AP-39429]"""
    log.info(
        "Testcase Started - Verify's that GET /api/v1/patients/ returns patients information successfully, when search string parameters are provided valid JWT cookies token is provided")

    log.info("Get patients request with  parameter ")
    res = mtb_web_service_valid_token.get(endpoints.GET_MTB_PATIENTS, get_default_headers(),
                                          {'searchString': search_by, 'perPage': 10})
    res_json = json.loads(res.text_payload)
    # Validating patient from response and parameter provided as patients first name, last name and mrn number
    if 'matchingPatients' in res_json.keys():
        patient_detail = res_json['matchingPatients'][0]
        # Checking given parameter value exist in a response
        valid_patient = search_by in patient_detail.values()
    assert 200 == res.status_code, "GET Patients status: %s" % res
    assert True == valid_patient, "GET Patients status: %s" % res
    log.info("Valid Patients found in response ")
    log.info("Tetscase Ended")


@pytest.mark.p0
@pytest.mark.p4
def test_get_patients_search_parameter_are_case_insensetive():
    """ automation testcase - Verify's that GET /api/v1/patients/ returns same patients information successfully, when case insensitive string provided and valid JWT cookies token is provided - [AP-39430]"""
    log.info(
        "Testcase Started - Verify's that GET /api/v1/patients/ returns same patients information successfully, when case insensitive string provided and valid JWT cookies token is provided")

    log.info("Get patients search request with same patient as parameter with different case insensitive value")
    # List value of case insensitive names
    patient_strings = [patient_info[0]['humanNameFirst'].lower(), patient_info[0]['humanNameFirst'].upper(),
                       patient_info[0]['humanNameFirst'].capitalize()]

    patient_mrns = []
    for i in patient_strings:
        res = mtb_web_service_valid_token.get(endpoints.GET_MTB_PATIENTS, get_default_headers(),
                                              {'searchString': i, 'perPage': 10})
        res_json = json.loads(res.text_payload)
        assert 200 == res.status_code, "GET Patients status: %s" % res
        # Validating patient from response and parameter provided as patients first name in lower, upper and capitalize case
        if 'matchingPatients' in res_json.keys():
            patient_detail = res_json['matchingPatients'][0]
            patient_mrns.append(patient_detail['mrn'])
    # Checking all mrn numbers are same
    valid_mrn = len(list(dict.fromkeys(patient_mrns))) == 1
    assert True == valid_mrn, "GET Patients status: %s" % res
    log.info("Valid Patients found in response ")
    log.info("Tetscase Ended")


@pytest.mark.p0
@pytest.mark.p4
def test_get_patients_search_parameter_are_partial_string():
    """ automation testcase - Verify's that GET /api/v1/patients/ returns same patients information successfully, when partial string provided and valid JWT cookies token is provided - [AP-39431]"""
    log.info(
        "Testcase Started - Verify's that GET /api/v1/patients/ returns same patients information successfully, when partial string provided and valid JWT cookies token is provided")

    log.info("Get patients search request with same patient as parameter with partial string values")
    # List of partial first name string
    patient_strings = [patient_info[0]['humanNameFirst'][:2], patient_info[0]['humanNameFirst'][:3],
                       patient_info[0]['humanNameFirst'][:4]]

    patient_mrns = []
    for i in patient_strings:
        res = mtb_web_service_valid_token.get(endpoints.GET_MTB_PATIENTS, get_default_headers(),
                                              {'searchString': i, 'perPage': 10})
        res_json = json.loads(res.text_payload)
        assert 200 == res.status_code, "GET Patients status: %s" % res
        # Validating patient from response and parameter provided as patients first name as partial string
        if 'matchingPatients' in res_json.keys():
            patient_detail = res_json['matchingPatients'][0]
            patient_mrns.append(patient_detail['mrn'])
    # Checking all mrn numbers are same
    valid_mrn = len(list(dict.fromkeys(patient_mrns))) == 1
    assert True == valid_mrn, "GET Patients status: %s" % res
    log.info("Valid Patients found in response ")
    log.info("Tetscase Ended")


@pytest.mark.p0
@pytest.mark.p4
@pytest.mark.skip(reason='no patients data in response')
def test_get_patients_search_parameter_using_korean_string():
    """ automation testcase - Verify's that GET /api/v1/patients/ returns same patients information successfully, when korean string provided and valid JWT cookies token is provided - [AP-39437]"""
    log.info(
        "Testcase Started - Verify's that GET /api/v1/patients/ returns same patients information successfully, when korean string provided and valid JWT cookies token is provided")

    log.info("Get patients search request with same patient as parameter with partial string values")
    patient_strings = ['아론']

    patient_mrns = []
    for i in patient_strings:
        res = mtb_web_service_valid_token.get(endpoints.GET_MTB_PATIENTS, get_default_headers(),
                                              {'searchString': i, 'perPage': 10})
        res_json = json.loads(res.text_payload)
        assert 200 == res.status_code, "GET Patients status: %s" % res
        if 'matchingPatients' in res_json.keys():
            patient_detail = res_json['matchingPatients'][0]
            patient_mrns.append(patient_detail['mrn'])
    valid_mrn = len(list(dict.fromkeys(patient_mrns))) == 1
    assert True == valid_mrn, "GET Patients status: %s" % res
    log.info("Valid Patients found in response ")
    log.info("Tetscase Ended")


test_data = [patient_info[0]['humanNameFirst'] + ' ' + patient_info[0]['humanNameLast'],
             patient_info[1]['humanNameFirst'] + ' ' + patient_info[1]['humanNameLast']]


@pytest.mark.p0
@pytest.mark.p4
@pytest.mark.parametrize("search_by", test_data)
def test_get_patients_multiple_parameter_values(search_by):
    """
    automation testcase - Verify's that GET /api/v1/patients/ returns patients information successfully,
    when patient first name, last name are provided and valid JWT cookies token is provided - [AP-39438]
    """
    log.info(
        "Testcase Started - Verify's that GET /api/v1/patients/ returns patients information successfully, "
        "when patient first name, last name are provided  valid JWT cookies token is provided"
    )

    log.info("Get patients request with first name and last name as parameter ")
    res = mtb_web_service_valid_token.get(endpoints.GET_MTB_PATIENTS, get_default_headers(),
                                          {'searchString': search_by, 'perPage': 10})
    res_json = json.loads(res.text_payload)
    if 'matchingPatients' in res_json.keys():
        patient_detail = res_json['matchingPatients'][0]
        valid_patient = search_by in patient_detail.values()
    assert 200 == res.status_code, "GET Patients status: %s" % res
    assert True == valid_patient, "GET Patients status: %s" % res
    log.info("Valid Patients found in response ")
    log.info("Tetscase Ended")


test_data = ["xxyyyzzzaaabbbzzzz", "00001111000011001"]


@pytest.mark.p0
@pytest.mark.p4
@pytest.mark.parametrize("search_by", test_data)
def test_get_patients_multiple_parameter_values(search_by):
    """
    automation testcase - Verify's that GET /api/v1/patients/ returns empty patients information successfully,
    when invalid name, invalid mrn are provided and valid JWT cookies token is provided - [AP-39439]
    """
    log.info(
        "Testcase Started - Verify's that GET /api/v1/patients/ returns empty patients information successfully, "
        "when invalid name, invalid mrn are provided  valid JWT cookies token is provided"
    )

    log.info("Get patients request with invalid name and invalid mrn")
    # Get request to get patient details with invalid name and mrn name
    res = mtb_web_service_valid_token.get(endpoints.GET_MTB_PATIENTS, get_default_headers(),
                                          {'searchString': search_by, 'perPage': 10})
    res_json = json.loads(res.text_payload)
    if 'matchingPatients' in res_json.keys():
        patient_detail = res_json['matchingPatients']
    # Validating in response we are getting empty value
    assert 200 == res.status_code, "GET Patients status: %s" % res
    assert [] == patient_detail, "GET Patients status: %s" % res
    log.info("Valid Patients found in response ")
    log.info("Tetscase Ended")


@pytest.mark.p0
def test_post_case_with_valid_patientId():
    """testcase method- Verify that (mtb-web) POST /case successful with valid patientID - [AP-39520]"""
    log.info("Testcase Started - Verify that (mtb-web) POST /case successful with valid patientID")
    log.info("Payload data generated, with valid PatientId data")
    data = {'patientId': patient_info[0]['patientId']}
    payload = json.dumps(data)
    log.info("Creating a new case using POST request with valid patientId using valid token")
    # Create case using patientID with valid token
    res = mtb_web_service_valid_cookies.post(endpoints.POST_CASES, payload,
                                             post_headers_content_json_accept_text())
    assert 201 == res.status_code, "CASE POST status: %s" % res
    log.info("New Case created successfully.")
    log.info("Testcase Ended")


@pytest.mark.p0
@pytest.mark.p4
def test_post_case_with_empty_patientId():
    """testcase method- Verify that (mtb-web) POST /case fails when empty patientID - [AP-39521]"""
    log.info("Testcase Started - Verify that (mtb-web) POST /case fails when empty patientID")
    log.info("Payload data generated, with empty PatientId data")
    data = {'patientId': ""}
    payload = json.dumps(data)
    log.info("Creating a new case using POST request with empty patientId using valid token")
    # Create case without patientID with valid token and empty patientId
    res = mtb_web_service_valid_token.post(endpoints.POST_CASES, payload,
                                           post_headers_content_json_accept_text())
    assert 400 == res.status_code, "CASE POST status: %s" % res
    log.info("Bad request error, PatientId is mandatory field")
    log.info("Testcase Ended")


@pytest.mark.p0
@pytest.mark.p4
def test_post_case_with_null_patientId():
    """testcase method- Verify that (mtb-web) POST /case fails when patientID is null- [AP-39522]"""
    log.info("Testcase Started - Verify that (mtb-web) POST /case fails when patientID is null")
    log.info("Payload data generated, with empty PatientId data")
    data = {'patientId': None}
    payload = json.dumps(data)
    log.info("Creating a new case using POST request with empty patientId using valid token")
    # Create case without patientID with valid token
    res = mtb_web_service_valid_token.post(endpoints.POST_CASES, payload,
                                           post_headers_content_json_accept_text())
    assert 400 == res.status_code, "CASE POST status: %s" % res
    log.info("Bad request error, PatientId value can not be null")
    log.info("Testcase Ended")


@pytest.mark.p0
@pytest.mark.skip(reason='Give 500 internal server error')
def test_post_case_attachment_with_valid_token():
    """ testcase method - Verify POST /case/<case_id>/attachment is successful with valid unexpired JWT token - [AP-39770]"""
    log.info("Testcase Started - Verify POST /case/<case_id>/attachment is successful with valid unexpired JWT token ")
    log.info("Payload data generated, Patient Id provided")
    data = {'patientId': patient_info[0]['patientId']}
    payload = json.dumps(data)
    log.info("Creating a new case using post request by providing patientId")
    get_uuid = mtb_web_service_valid_cookies.post(endpoints.POST_CASES, payload,
                                                  post_headers_content_json_accept_text())

    log.info("New Case created successfully")
    uuid = json.loads(get_uuid.text_payload)["uuid"]
    log.info("Generating payload data for attachment file ")
    data = {'exampleProp': 'replace me with the real contract'}
    payload = json.dumps(data)
    log.info("Case attachment file payload using POST request with valid token")
    res = mtb_web_service_valid_cookies.post(endpoints.POST_CASE_ATTACHMENT % uuid, payload,
                                             {'Accept': '*/*', 'Content-Type': 'multipart/formdata'})
    assert 201 == res.status_code, "CASE POST status: %s" % res
    log.info("Attachment for case created successfully...")
    log.info("Testcase Ended")


@pytest.mark.p0
@pytest.mark.skip(reason='Empty token 200 Sing in Auth0 response, expected 401 unauthorized error')
def test_post_case_attachment_with_empty_token():
    """ testcase method - Verify POST /case/<case_id>/attachment fails with empty JWT token - [AP-39771]"""
    log.info("Testcase Started - Verify POST /case/<case_id>/attachment fails with empty JWT token ")
    log.info("Payload data generated, Patient Id provided")
    data = {'patientId': patient_info[0]['patientId']}
    payload = json.dumps(data)
    log.info("Creating a new case using post request by providing patientId")
    get_uuid = mtb_web_service_valid_cookies.post(endpoints.POST_CASES, payload,
                                                  post_headers_content_json_accept_text())

    log.info("New Case created successfully")
    uuid = json.loads(get_uuid.text_payload)["uuid"]
    log.info("Generating payload data for attachment file ")
    data = {'exampleProp': 'replace me with the real contract'}
    payload = json.dumps(data)
    log.info("Case attachment file payload using POST request with valid token")
    res = mtb_web_service_empty_token.post(endpoints.POST_CASE_ATTACHMENT % uuid, payload,
                                           {'Accept': '*/*', 'Content-Type': 'multipart/formdata'})
    assert 401 == res.status_code, "CASE POST status: %s" % res
    log.info("Attachment for case created successfully...")
    log.info("Testcase Ended")

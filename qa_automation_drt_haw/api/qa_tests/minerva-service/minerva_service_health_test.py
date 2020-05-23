import pytest
from qa_automation_drt_haw.api.api_utils.serviceApi import ServiceAPI, ServiceInfo, Token
from qa_automation_core.api.service import Service
from qa_automation_core.api.api_headers import (get_default_headers, put_default_headers,
                                                post_default_headers, post_headers_content_json_accept_text)
from endpoints_minerva import endpoints
import json
import base64
import string
import re
from datetime import date
from qa_automation_drt_haw.ui.ui_utils.Logs import log
from qa_automation_drt_haw.settings import Config
from qa_automation_drt_haw.api.qa_test_data.data_generator import Data_Generator

"""Data_Generator Class - Generating string for patients search and string patient information to use in testcase methods"""
patient_info = Data_Generator('mtb').patients_info

username = Config.portal_2_roles_username
psw = Config.portal_2_roles_password

minerva_service_info = ServiceInfo('minerva-service')
mtb_info = ServiceInfo('mtb-web')
valid_jwt = Token(username, psw)

minerva_service_empty_token = Service(minerva_service_info.url, token="", sslcert=False)
minerva_service_invalid_token = Service(minerva_service_info.url, token="8594389jijfi49", sslcert=False)
minerva_service_expired_token = Service(minerva_service_info.url, token="8594389jijfi49", sslcert=False)
minerva_service_valid_token = Service(minerva_service_info.url, token=str(valid_jwt), sslcert=False)

mtb_web_service_empty_token = Service(mtb_info.url, token="", sslcert=False)
mtb_web_service_valid_token = Service(mtb_info.url, jwt_cookie=str(valid_jwt), sslcert=False)

regex = re.compile('[@_!#$%^&*()<>?/|}{~:]')


@pytest.mark.p0
@pytest.mark.p4
def test_healthcheck_alive():
    """ automation testcase - Verify's that GET /v1/health/alive successful or API connection alive , when valid JWT token is provided """
    log.info(
        "Testcase Started - Verify's that GET /v1/health/alive successful or API connection alive , when valid JWT token is provided")
    log.info("Checking Minerva Service Connection Status")
    res = minerva_service_valid_token.get(endpoints.HEALTH_ALIVE, get_default_headers())
    log.info("Minerva Service connection status: %s", res.status_code)
    assert 200 == res.status_code, "ALIVE status: %s" % res.status_code
    log.info("Testcase Ended")


@pytest.mark.p0
@pytest.mark.p4
def test_healthcheck_ready():
    """ automation testcase - Verify's that GET /v1/health/ready successful or API connection ready , when valid JWT token is provided """
    log.info(
        "Testcase Started - Verify's that GET /v1/health/ready successful or API connection ready , when valid JWT token is provided ")
    log.info("Checking Minerva Service Connection Ready")
    res = minerva_service_valid_token.get(endpoints.HEALTH_READY, get_default_headers())
    assert 200 == res.status_code, "READY status: %s" % res.status_code
    log.info("Minerva Service Connection is Ready")
    log.info("Testcase Ended")


@pytest.mark.p0
def test_post_case_attachment_with_empty_token():
    """ testcase method - Verify POST /case/<case_id>/attachment fails without JWT token """
    log.info("Testcase Started - Verify POST /case/<case_id>/attachment fails without JWT token")
    log.info("Payload data generated, Patient Id provided")
    data = {'patientId': patient_info[0]['patientId']}
    payload = json.dumps(data)
    log.info("Creating a new case using post request by providing patientId")
    get_uuid = minerva_service_valid_token.post(endpoints.POST_CASES, payload,
                                                post_headers_content_json_accept_text())

    log.info("New Case created successfully")
    uuid = get_uuid.text_payload
    log.info("Generating payload data for attachment file ")
    data = {'fileData': str(base64.b64encode('my_pdf.pdf'.encode("utf-8")), "utf-8"), 'fileName': 'my_pdf.pdf',
            'fileType': 'pdf'}
    payload = json.dumps(data)
    log.info("Case attachment file payload using POST request with empty token")
    res = minerva_service_empty_token.post(endpoints.POST_CASE_ATTACHMENT % uuid, payload,
                                           post_default_headers())
    assert 401 == res.status_code, "CASE POST status: %s" % res
    log.info("Getting Unauthorized Response")
    log.info("Testcase Ended")


@pytest.mark.p0
def test_post_case_attachment_with_valid_token():
    """ testcase method - Verify POST /case/<case_id>/attachment is successful with valid unexpired JWT token """
    log.info("Testcase Started - Verify POST /case/<case_id>/attachment is successful with valid unexpired JWT token ")
    log.info("Payload data generated, Patient Id provided")
    data = {'patientId': patient_info[0]['patientId']}
    payload = json.dumps(data)
    log.info("Creating a new case using post request by providing patientId")
    get_uuid = minerva_service_valid_token.post(endpoints.POST_CASES, payload,
                                                post_headers_content_json_accept_text())

    log.info("New Case created successfully")
    uuid = get_uuid.text_payload
    log.info("Generating payload data for attachment file ")
    data = {'fileData': str(base64.b64encode('my_pdf.pdf'.encode("utf-8")), "utf-8"), 'fileName': 'my_pdf.pdf',
            'fileType': 'pdf'}
    payload = json.dumps(data)
    log.info("Case attachment file payload using POST request with valid token")
    res = minerva_service_valid_token.post(endpoints.POST_CASE_ATTACHMENT % uuid, payload,
                                           post_default_headers())
    assert 201 == res.status_code, "CASE POST status: %s" % res
    log.info("Attachment for case created successfully...")
    log.info("Testcase Ended")


@pytest.mark.p0
def test_get_case_uuid_with_valid_token():
    """ Verify that GET /case/uuid is successful when valid unexpired JWT token is provided """
    log.info("Testcase Started - Verify that GET /case/uuid is successful when valid unexpired JWT token is provided")
    log.info("Payload data generated, Patient Id provided")
    data = {'patientId': patient_info[0]['patientId']}
    payload = json.dumps(data)
    log.info("Creating a new case using post request by providing patientId")
    res = minerva_service_valid_token.post(endpoints.POST_CASES, payload,
                                           post_headers_content_json_accept_text())
    assert 201 == res.status_code, "CASE POST status: %s" % res
    log.info("New case using post request by providing patientId created successfully.")

    casesId = res.text_payload
    log.info("Get CASE details using GET Request and caseId as parameter with valid token")
    res = minerva_service_valid_token.get(endpoints.GET_CASE_UUID + casesId, get_default_headers())
    assert 200 == res.status_code, "GET CASE by UUID status: %s" % res
    log.info("Fetched case details successfully")
    log.info("Testcase Ended")


@pytest.mark.p0
@pytest.mark.p4
def test_post_case_with_empty_token():
    """testcase method- Verify that (minerva-service) POST /case fails without JWT token"""
    log.info("Testcase Started - Verify that (minerva-service) POST /case fails without JWT token")
    log.info("Payload data generated, Patient Id provided")
    data = {'patientId': patient_info[0]['patientId']}
    payload = json.dumps(data)
    log.info("Creating a new case using POST request by providing patientId with empty token")
    res = minerva_service_empty_token.post(endpoints.POST_CASES, payload,
                                           post_headers_content_json_accept_text())
    assert 401 == res.status_code, "CASE POST status: %s" % res
    log.info("Getting Unauthorized Response")
    log.info("Testcase Ended")


@pytest.mark.p0
# TODO - Move testcase in seprate suite file e.g create file minerva_service_cases_test.py
def test_get_case_uuid_with_empty_token():
    """ automation testcase - Verify's that GET /case/uuid fails, when JWT token is not provided """
    log.info("Testcase Started - Verify's that GET /case/uuid fails, when JWT token is not provided")
    log.info("Payload data generated, Patient Id provided")
    data = {'patientId': patient_info[0]['patientId']}
    payload = json.dumps(data)
    log.info("Creating a new case using POST request by providing patientId with valid token")
    res = minerva_service_valid_token.post(endpoints.POST_CASES, payload,
                                           post_headers_content_json_accept_text())
    assert 201 == res.status_code, "CASE POST status: %s" % res
    log.info("New case using post request by providing patientId created successfully.")

    casesId = res.text_payload
    log.info("Get CASE details using GET Request and caseId as parameter with empty token")
    res = minerva_service_empty_token.get(endpoints.GET_CASE_UUID + casesId, get_default_headers())
    assert 401 == res.status_code, "GET CASE by UUID status: %s" % res
    log.info("Getting Unauthorized Response")
    log.info("Testcase Ended")


@pytest.mark.p0
# TODO - Move testcase in seprate suite file e.g create file minerva_service_cases_test.py
def test_post_case_with_valid_token():
    """ automation testcase - Verify's that POST /v1/case or create case successful, when valid JWT token is provided"""
    log.info(
        "Testcase Started - Verify's that POST /v1/case or create case successful, when valid JWT token is provided")
    log.info("Payload data generated, Patient Id provided")
    data = {'patientId': patient_info[0]['patientId']}
    payload = json.dumps(data)
    log.info("Creating a new case using POST request by providing patientId with valid token")
    res = minerva_service_valid_token.post(endpoints.POST_CASES, payload, post_headers_content_json_accept_text())
    assert 201 == res.status_code, "CASE POST status: %s" % res
    log.info("New case using post request by providing patientId created successfully.")
    log.info("Testcase Ended")


# MTB Attachment Testcases -------------
@pytest.mark.p0
def test_post_case_attachment_with_invalid_case_id():
    """ testcase method - Verify POST /case/<case_id>/attachment fails with invalid caseID - AP-39814 """
    log.info("Testcase Started - Verify POST /case/<case_id>/attachment fails with invalid caseID")
    log.info("Payload data generated, Patient Id provided")
    data = {}
    data['patientId'] = patient_info[0]['patientId']
    payload = json.dumps(data)
    # Create new case using patientId detail to case uuid or caseID
    log.info("Creating a new case using POST request by providing patientId with valid token")
    get_uuid = minerva_service_valid_token.post(endpoints.POST_CASES, payload,
                                                post_headers_content_json_accept_text())
    log.info("New Case created successfully and change the value of uuid(invalid)")
    uuid = get_uuid.text_payload + 'iJkR123'
    # Payload data provided for attachment for files(docs) using wrong uuid ID
    log.info("Generating payload data for attachment file ")
    data = {}
    data['fileData'] = str(base64.b64encode('my_pdf.pdf'.encode("utf-8")), "utf-8")
    data['fileName'] = 'my_pdf.pdf'
    data['fileType'] = 'pdf'
    payload = json.dumps(data)
    log.info("Case attachment file payload using POST request with valid token and invalid uuid")
    res = minerva_service_valid_token.post(endpoints.POST_CASE_ATTACHMENT % uuid, payload,
                                           post_default_headers())
    res_error = "Unable to save file attachment, case Id: %s not present." % uuid
    assert res_error == res.json_payload, "CASE ATTACHMENT POST status: %s" % res
    assert 500 == res.status_code, "CASE ATTACHMENT POST status: %s" % res
    log.info("Getting Internal Server Error in Response")
    log.info("Testcase Ended")


@pytest.mark.p0
def test_post_case_attachment_without_required_field():
    """ testcase method - Verify POST /case/<case_id>/attachment fails without required field - AP-39817"""
    log.info("Testcase Started - Verify POST /case/<case_id>/attachment fails without required field")
    log.info("Payload data generated, Patient Id provided")
    data = {}
    data['patientId'] = patient_info[0]['patientId']
    payload = json.dumps(data)
    # Create new case using patientId detail to case uuid or caseID
    log.info("Creating a new case using POST request by providing patientId with valid token")
    get_uuid = minerva_service_valid_token.post(endpoints.POST_CASES, payload,
                                                post_headers_content_json_accept_text())
    log.info("New Case created successfully.")
    uuid = get_uuid.text_payload

    log.info("Generating payload data for attachment file without required field")
    data = {}
    data['fileData'] = str(base64.b64encode('my_pdf.pdf'.encode("utf-8")), "utf-8")
    data['fileType'] = 'pdf'
    payload = json.dumps(data)
    # Payload data provided for attachment for files(docs) without mandatory field
    log.info("Case attachment file payload using POST request with valid token")
    res = minerva_service_valid_token.post(endpoints.POST_CASE_ATTACHMENT % uuid, payload,
                                           post_default_headers())
    assert "Unable to save file attachment, failed in file-service POST" == res.json_payload, "CASE ATTACHMENT POST status: %s" % res
    assert 500 == res.status_code, "CASE ATTACHMENT POST status: %s" % res
    log.info("Getting Internal Server Error in Response")
    log.info("Testcase Ended")


@pytest.mark.p0
def test_post_case_attachment_with_required_field_empty_value():
    """ testcase method - Verify POST /case/<case_id>/attachment fails with required fields empty string value - AP-39818"""
    log.info("Testcase Started - Verify POST /case/<case_id>/attachment fails with required fields empty string value")
    log.info("Payload data generated, Patient Id provided")
    data = {}
    data['patientId'] = patient_info[0]['patientId']
    payload = json.dumps(data)
    # Create new case using patientId detail to case uuid or caseID
    log.info("Creating a new case using POST request by providing patientId with valid token")
    get_uuid = minerva_service_valid_token.post(endpoints.POST_CASES, payload,
                                                post_headers_content_json_accept_text())

    uuid = get_uuid.text_payload
    log.info("New Case created successfully.")
    log.info("Generating payload data for attachment file with empty required field")
    data = {}
    data['fileData'] = str(base64.b64encode('my_pdf.pdf'.encode("utf-8")), "utf-8")
    data['fileName'] = ""
    data['fileType'] = 'pdf'
    payload = json.dumps(data)
    # Payload data provided for attachment for files(docs) with mandatory field empty value
    log.info("Case attachment file payload using POST request with valid token")
    res = minerva_service_valid_token.post(endpoints.POST_CASE_ATTACHMENT % uuid, payload,
                                           post_default_headers())
    assert "Unable to save file attachment, failed in file-service POST" == res.json_payload, "CASE ATTACHMENT POST status: %s" % res
    assert 500 == res.status_code, "CASE ATTACHMENT POST status: %s" % res
    log.info("Getting Internal Server Error in Response")
    log.info("Testcase Ended")


# MTB Attachments Testcases ends ---------------


# MTB Cases Testcases Start ----------------
@pytest.mark.p0
@pytest.mark.skip(reason='wrong message in response')
def test_post_case_with_invalid_token():
    """testcase method - Verify that (minerva-service) POST /case fails with invalid JWT token - AP-37867"""
    log.info("Testcase Started - Verify that (minerva-service) POST /case fails with invalid JWT token")
    log.info("Payload data generated, Patient Id provided")
    data = {'patientId': patient_info[0]['patientId']}
    payload = json.dumps(data)
    # Create case using patientID with invalid token
    log.info("Creating a new case using POST request by providing patientId with invalid token")
    res = minerva_service_invalid_token.post(endpoints.POST_CASES, payload,
                                             post_headers_content_json_accept_text())
    assert 401 == res.status_code, "CASE POST status: %s" % res
    # TODO response message is 'Failed to decode token' in JIRA ticket 'Unable to find appropriate key.' is mentioned.
    assert res.json_payload == {'message': "('Failed to decode token.', 401)"}, "CASE POST status: %s" % res
    log.info("Getting Unauthorized Response - fail to decode token in Response")
    log.info("Testcase Ended")


@pytest.mark.p0
def test_get_case_uuid_with_valid_uuid():
    """ Verify that GET /case/uuid is successful when valid uuid is provided - AP-38027"""
    log.info("Testcase Started - Verify that GET /case/uuid is successful when valid uuid is provided")
    log.info("Payload data generated, Patient Id provided")
    data = {'patientId': patient_info[0]['patientId']}
    payload = json.dumps(data)
    # Create case using patientID with valid token
    log.info("Creating a new case using POST request by providing patientId with valid token")
    res = minerva_service_valid_token.post(endpoints.POST_CASES, payload,
                                           post_headers_content_json_accept_text())
    assert 201 == res.status_code, "CASE POST status: %s" % res

    casesId = res.text_payload
    # Response verify using valid caseID
    log.info("Validating case using valid caseId as parameter in GET request")
    res = minerva_service_valid_token.get(endpoints.GET_CASE_UUID + casesId, get_default_headers())
    assert 200 == res.status_code, "GET CASE by UUID status: %s" % res
    log.info("Validated response successfully")
    log.info("Testcase Ended")


@pytest.mark.p0
def test_get_case_uuid_with_invalid_uuid():
    """ Verify that GET /case/uuid fails when invalid uuid is provided - AP-38028"""
    log.info("Testcase Started - Verify that GET /case/uuid fails when invalid uuid is provided")
    log.info("Payload data generated, Patient Id provided")
    data = {'patientId': patient_info[0]['patientId']}
    payload = json.dumps(data)
    # Create case using patientID with valid token
    log.info("Creating a new case using POST request by providing patientId with valid token")
    res = minerva_service_valid_token.post(endpoints.POST_CASES, payload,
                                           post_headers_content_json_accept_text())
    assert 201 == res.status_code, "CASE POST status: %s" % res

    casesId = res.text_payload + 'iJkR123'
    log.info("New Case created successfully and making valid caseId to invalid caseId")
    # Response verify using invalid caseID
    log.info("Validating case using invalid caseId as parameter in GET request")
    res = minerva_service_valid_token.get(endpoints.GET_CASE_UUID + casesId, get_default_headers())
    assert 404 == res.status_code, "GET CASE by invalid UUID status: %s" % res
    assert "Couldn't find a case for this case_id" == res.json_payload, "GET CASE by invalid UUID status: %s" % res
    log.info("Getting data not found error in Response")
    log.info("Testcase Ended")


@pytest.mark.p0
def test_get_case_uuid_with_invalid_token():
    """ Verify that GET /case/uuid is fails when invalid JWT token is provided - AP-39495"""
    log.info("Testcase Started - Verify that GET /case/uuid is fails when invalid JWT token is provided")
    log.info("Payload data generated, Patient Id provided")
    data = {'patientId': patient_info[0]['patientId']}
    payload = json.dumps(data)
    # Create case using patientID with valid token
    log.info("Creating a new case using POST request by providing patientId with valid token")
    res = minerva_service_valid_token.post(endpoints.POST_CASES, payload,
                                           post_headers_content_json_accept_text())
    assert 201 == res.status_code, "CASE POST status: %s" % res

    casesId = res.text_payload
    log.info("New Case created successfully.")
    # Response verify using invalid token
    log.info("Validating case using valid caseId as parameter in GET request with invalid token")
    res = minerva_service_invalid_token.get(endpoints.GET_CASE_UUID + casesId, get_default_headers())
    assert {'message': "('Failed to decode token.', 401)"} == res.json_payload, "GET CASE by UUID status: %s" % res
    assert 401 == res.status_code, "GET CASE by UUID status: %s" % res
    log.info("Getting Unauthorized Response - fail to decode token in Response")
    log.info("Testcase Ended")


@pytest.mark.p0
@pytest.mark.p4
def test_post_case_attachment_with_empty_patient_id():
    """ testcase method - Verify POST /case/<case_id>/attachment fails with empty patientID - AP-39501 """
    log.info("Testcase Started - Verify POST /case/<case_id>/attachment fails with empty patientID")
    log.info("Payload data generated, with empty Patient Id data")
    data = {'patientId': ""}
    payload = json.dumps(data)
    # Create case using patientID empty value
    log.info("Creating a new case using POST request without patientId using valid token")
    res = minerva_service_valid_token.post(endpoints.POST_CASES, payload,
                                           post_headers_content_json_accept_text())
    res_json = json.loads(res.text_payload)

    assert 400 == res.status_code, "POST CASE without patientId status: %s" % res
    assert "'' is too short - 'patientId'" == res_json["detail"], "POST CASE without patientId status: %s" % res
    log.info("Getting Bad Request error in  Response")
    log.info("Testcase Ended")


# MTB Cases Testcases ends ------------------

# MTB Minerva Set2 API starts
@pytest.mark.p0
def test_get_case_uuid_with_valid_expired_token():
    """ Verify that GET /case/uuid fails when valid expired JWT token is provided - [AP-AP-37774]"""
    log.info("Testcase Started - Verify that GET /case/uuid fails when valid expired JWT token is provided")
    log.info("Payload data generated, with valid Patient Id data")
    data = {'patientId': patient_info[0]['patientId']}
    payload = json.dumps(data)

    log.info("Creating a new case using POST request with valid patientId using valid token")
    # Create case using patientID with valid token
    res = minerva_service_valid_token.post(endpoints.POST_CASES, payload,
                                           post_headers_content_json_accept_text())
    assert 201 == res.status_code, "CASE POST status: %s" % res

    log.info("New Case created successfully.")
    log.info("Validating case using valid caseId as parameter in GET request with expired/invalid token")
    casesId = res.text_payload
    # Validating caseId using invalid token in GET request
    res = minerva_service_invalid_token.get(endpoints.GET_CASE_UUID + casesId, get_default_headers())
    assert 401 == res.status_code, "GET CASE by UUID status: %s" % res
    assert res.json_payload == {'message': "('Failed to decode token.', 401)"}
    log.info("Getting Unauthorized Response - fail to decode token in Response")
    log.info("Testcase Ended")


@pytest.mark.p0
@pytest.mark.p4
def test_get_cases_with_valid_unexpired_token():
    """ Verify that GET /cases returns array value of cases when valid unexpired JWT token is provided - [AP-37759]"""
    log.info(
        "Testcase Started - Verify that GET /cases returns array value of cases when valid unexpired JWT token is provided")
    log.info("Fetching cases details using GET request with valid token")
    cases = minerva_service_valid_token.get(endpoints.GET_CASES, get_default_headers())
    assert 200 == cases.status_code, "GET Cases status: %s" % cases
    log.info("Fetched all cases")
    log.info("Testcase Ended")


@pytest.mark.p0
@pytest.mark.p4
def test_post_case_with_invalid_patientId():
    """testcase method- Verify that (minerva-service) POST /case fails with invalid patientID - [AP-37695]"""
    log.info("Testcase Started - Verify that (minerva-service) POST /case fails with invalid patientID")
    log.info("Payload data generated, with invalid Patient Id data")
    data = {'patientId': patient_info[0]['patientId'] + 'xyz123'}
    payload = json.dumps(data)
    log.info("Creating a new case using POST request with invalid patientId using valid token")
    # Create case using invalid patientID with valid token
    res = minerva_service_valid_token.post(endpoints.POST_CASES, payload,
                                           post_headers_content_json_accept_text())

    assert 422 == res.status_code, "CASE POST status: %s" % res
    assert "Unable to fetch the patient" == res.text_payload, "CASE POST status: %s" % res
    log.info("Unable to fetch the patient, Patient not found error")
    log.info("Testcase Ended")


@pytest.mark.p0
def test_post_case_with_valid_patientId():
    """testcase method- Verify that (minerva-service) POST /case successful with valid patientID - [AP-37691]"""
    log.info("Testcase Started - Verify that (minerva-service) POST /case successful with valid patientID")
    log.info("Payload data generated, with valid PatientId data")
    data = {'patientId': patient_info[0]['patientId']}
    payload = json.dumps(data)
    log.info("Creating a new case using POST request with valid patientId using valid token")
    # Create case using patientID with valid token
    res = minerva_service_valid_token.post(endpoints.POST_CASES, payload,
                                           post_headers_content_json_accept_text())
    assert 201 == res.status_code, "CASE POST status: %s" % res
    log.info("New Case created successfully.")
    log.info("Testcase Ended")


@pytest.mark.p0
@pytest.mark.p4
def test_post_case_with_empty_patientId():
    """testcase method- Verify that (minerva-service) POST /case fails when empty patientID - [AP-37671]"""
    log.info("Testcase Started - Verify that (minerva-service) POST /case fails when empty patientID")
    log.info("Payload data generated, with empty PatientId data")
    data = {'patientId': ''}
    payload = json.dumps(data)
    log.info("Creating a new case using POST request with empty patientId using valid token")
    # Create case without patientID with valid token
    res = minerva_service_valid_token.post(endpoints.POST_CASES, payload,
                                           post_headers_content_json_accept_text())
    assert 400 == res.status_code, "CASE POST status: %s" % res
    log.info("Bad request error, PatientId is mandatory field")
    log.info("Testcase Ended")


@pytest.mark.p0
def test_get_case_auto_report_with_valid_token():
    """ Verify that GET /case/caseId/autoreports is successful when valid unexpired token is  provided - AP-39988"""
    log.info(
        "Testcase Started - Verify that GET /case/caseId/autoreports is successful when valid unexpired token is  provided")
    log.info("Payload data generated, with valid PatientId data")
    data = {'patientId': patient_info[0]['patientId']}
    payload = json.dumps(data)
    # Create case using patientID with valid token
    log.info("Creating a new case using POST request with valid patientId using valid token")
    res = minerva_service_valid_token.post(endpoints.POST_CASES, payload,
                                           post_headers_content_json_accept_text())
    assert 201 == res.status_code, "CASE POST status: %s" % res
    log.info("New Case created successfully.")

    caseId = res.text_payload
    log.info("Fetching auto reports details using GET request by providing valid caseId")
    auto_reports = minerva_service_valid_token.get(endpoints.GET_AUTO_REPORTS % caseId, get_default_headers())
    # TODO no auto reports are present in database
    assert 200 == auto_reports.status_code, "GET Auto Reports status: %s" % auto_reports
    log.info("Fetched all auto reports related to caseId")
    log.info("Testcase Ended")


@pytest.mark.p0
@pytest.mark.skip(reason='Need to fetch caseId from database for different organization')
def test_post_case_attachment_with_case_id_from_different_org():
    """ testcase method - Verify POST /case/<case_id>/attachment fails with invalid caseID - AP-39814 """
    log.info("Testcase Started - Verify POST /case/<case_id>/attachment fails with invalid caseID")
    log.info("Payload data generated, with valid PatientId data")
    data = {'patientId': patient_info[0]['patientId']}
    payload = json.dumps(data)
    # Create new case using patientId detail to case uuid or caseID
    log.info("Creating a new case using POST request with valid patientId using valid token")
    get_uuid = minerva_service_valid_token.post(endpoints.POST_CASES, payload,
                                                post_headers_content_json_accept_text())

    uuid = Config.integration2  # TODO fetch it from database directly it belongs to integration2 org or create a different user for it
    # Payload data provided for attachment for files(docs) using wrong uuid ID
    data = {'fileData': str(base64.b64encode('my_pdf.pdf'.encode("utf-8")), "utf-8"), 'fileName': 'my_pdf.pdf',
            'fileType': 'pdf'}
    payload = json.dumps(data)
    log.info("Case attachment file payload with caseID from different organization using POST request with valid token")
    res = minerva_service_valid_token.post(endpoints.POST_CASE_ATTACHMENT % uuid, payload,
                                           post_default_headers())
    assert "Unauthorized" == res.json_payload, "CASE ATTACHMENT POST status: %s" % res
    assert 401 == res.status_code, "CASE ATTACHMENT POST status: %s" % res
    log.info("Getting Unauthorized error.")
    log.info("Testcase Ended")


# MTB Minerva Set2 API ends

# Minerva Service Set3 API starts

@pytest.mark.p0
@pytest.mark.p4
def test_post_case_with_expired_token():
    """testcase method - Verify that (minerva-service) POST /case fails with expired JWT token - AP-37866"""
    log.info("Testcase Started - Verify that (minerva-service) POST /case fails with expired JWT token")
    log.info("Payload data generated, Patient Id provided")
    data = {'patientId': patient_info[0]['patientId']}
    payload = json.dumps(data)
    # Create case using patientID with invalid token
    log.info("Creating a new case using POST request by providing patientId with invalid token")
    res = minerva_service_expired_token.post(endpoints.POST_CASES, payload,
                                             post_headers_content_json_accept_text())
    assert 401 == res.status_code, "CASE POST status: %s" % res
    assert res.json_payload == {'message': "('Failed to decode token.', 401)"}, "CASE POST status: %s" % res
    log.info("Getting Unauthorized Response - fail to decode token in Response")
    log.info("Testcase Ended")


@pytest.mark.p0
def test_put_case_form_add_manual_report_with_valid_token():
    """testcase method - Verify PUT request adding manual report to case form - AP-39926"""
    log.info("Testcase Started -Verify PUT request adding manual report to case form")
    log.info("Payload data generated, with valid PatientId data")
    data = {'patientId': patient_info[0]['patientId']}
    payload = json.dumps(data)
    # Create case using patientID with valid token
    log.info("Creating a new case using POST request with valid patientId using valid token")
    res = minerva_service_valid_token.post(endpoints.POST_CASES, payload,
                                           post_headers_content_json_accept_text())
    assert 201 == res.status_code, "CASE POST status: %s" % res
    log.info("New Case created successfully.")

    caseId = res.text_payload
    log.info("Get CASE details using GET Request and caseId as parameter with valid token")
    res = minerva_service_valid_token.get(endpoints.GET_CASE_UUID + caseId, get_default_headers())
    assert 200 == res.status_code, "GET CASE by UUID status: %s" % res
    log.info("Fetched case details successfully")
    data = res.json_payload
    log.info("adding manual report data to verify PUT request")
    # Providing manual report value to add new report data also today's date function added
    data["CaseForm"]["molecularResultsSummary"]["manualReports"] = [{"alterationDetails": [], "fileInfo": {},
                                                                     "reportDate": str(date.today()),
                                                                     "reportName": "Tempus xT Report",
                                                                     "uuid": caseId}]
    payload = json.dumps(data)
    log.info("PUT request to add manual report to case form using CaseID")
    res = minerva_service_valid_token.put(endpoints.PUT_CASE_FORM_UUID % caseId, payload, put_default_headers())
    assert 200 == res.status_code, "PUT CASE FORM by UUID status: %s" % res
    log.info("Added manual report successfully")


@pytest.mark.p0
def test_put_case_form_edit_manual_report_with_valid_token():
    """testcase method - Verify PUT request editing manual report to case form"""
    log.info("Testcase Started - Verify PUT request adding manual report to case form ")
    log.info("Payload data generated, with valid PatientId data")
    data = {'patientId': patient_info[0]['patientId']}
    payload = json.dumps(data)
    # Create case using patientID with valid token
    log.info("Creating a new case using POST request with valid patientId using valid token")
    res = minerva_service_valid_token.post(endpoints.POST_CASES, payload,
                                           post_headers_content_json_accept_text())
    assert 201 == res.status_code, "CASE POST status: %s" % res
    log.info("New Case created successfully.")

    caseId = res.text_payload
    log.info("Get CASE details using GET Request and caseId as parameter with valid token")
    res = minerva_service_valid_token.get(endpoints.GET_CASE_UUID + caseId, get_default_headers())
    assert 200 == res.status_code, "GET CASE by UUID status: %s" % res
    log.info("Fetched case details successfully")

    data = res.json_payload
    log.info("editing manual report data to verify PUT request")
    # Providing manual report to change existing value also today's date function added
    data["CaseForm"]["molecularResultsSummary"]["manualReports"] = [
        {"alterationDetails": [], "fileInfo": {}, "reportDate": str(date.today()),
         "reportName": "Tempus1 xT Report", "uuid": caseId}]
    payload = json.dumps(data)
    log.info("PUT request to edit manual report to case form using CaseID")
    res = minerva_service_valid_token.put(endpoints.PUT_CASE_FORM_UUID % caseId, payload, put_default_headers())
    assert 200 == res.status_code, "PUT CASE FORM by UUID status: %s" % res
    log.info("Edited manual report successfully")


@pytest.mark.p0
def test_put_case_form_delete_manual_report_with_valid_token():
    """testcase method - Verify PUT request deleting manual report to case form"""
    log.info("Testcase Started - Verify PUT request deleting manual report to case form")
    log.info("Payload data generated, with valid PatientId data")
    data = {'patientId': patient_info[0]['patientId']}
    payload = json.dumps(data)
    # Create case using patientID with valid token
    log.info("Creating a new case using POST request with valid patientId using valid token")
    res = minerva_service_valid_token.post(endpoints.POST_CASES, payload,
                                           post_headers_content_json_accept_text())
    assert 201 == res.status_code, "CASE POST status: %s" % res
    log.info("New Case created successfully.")

    caseId = res.text_payload
    log.info("Get CASE details using GET Request and caseId as parameter with valid token")
    res = minerva_service_valid_token.get(endpoints.GET_CASE_UUID + caseId, get_default_headers())
    assert 200 == res.status_code, "GET CASE by UUID status: %s" % res
    log.info("Fetched case details successfully")

    data = res.json_payload
    log.info("editing manual report data to verify PUT request")
    # Providing manual report blank to remove manual report
    data["CaseForm"]["molecularResultsSummary"]["manualReports"] = []
    payload = json.dumps(data)
    log.info("PUT request to delete manual report to case form using CaseID")
    res = minerva_service_valid_token.put(endpoints.PUT_CASE_FORM_UUID % caseId, payload, put_default_headers())

    assert 200 == res.status_code, "PUT CASE FORM by UUID status: %s" % res
    log.info("Deleted manual report successfully")

# Minerva Service Set3 API ends

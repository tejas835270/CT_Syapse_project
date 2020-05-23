import pytest
from qa_automation_drt_haw.settings import Config
from qa_automation_drt_haw.api.api_utils.serviceApi import ServiceAPI, ServiceInfo, Token
from qa_automation_core.api.service import Service
from qa_automation_core.api.api_headers import (get_default_headers,
                                                post_default_headers, post_headers_content_json_accept_text)
from qa_automation_core.api.api_response import ApiResponse
from qa_automation_drt_haw.ui.ui_utils.Logs import log
from qa_automation_drt_haw.api.qa_test_data.data_generator import Data_Generator
from endpoints_oncology import endpoints
import re
import string
import json

"""Data_Generator Class - Generating string for patients search and string patient information to use in testcase methods"""
patient_info = Data_Generator('oncology').patients_info

username = Config.portal_2_roles_username
psw = Config.portal_2_roles_password


oncology_info = ServiceInfo('oncology-web')
valid_jwt = Token(username, psw)
portal_info = ServiceInfo('portal-web')


onc_web_service_valid_token = Service(oncology_info.url, jwt_cookie=str(valid_jwt), sslcert=False)
onc_web_service_empty_token = Service(oncology_info.url, token="", sslcert=False)
# TODO expired token
expired_jwt = ""
onc_web_service_expired_token = Service(portal_info.url, token=str("8594389jijfi49"), sslcert=False)

regex = re.compile('[@_!#$%^&*()<>?/|}{~:]')

@pytest.mark.p0
@pytest.mark.p4
def test_healthcheck_alive():
    """ automation testcase - Verify's that GET /alive or API connection alive , when valid JWT cookies token is provided """
    log.info("Testcase Started - Verify's that GET /alive or API connection alive , when valid JWT cookies token is provided")
    log.info("Checking Oncology web Connection Status")
    res = onc_web_service_valid_token.get(endpoints.HEALTH_ALIVE, get_default_headers())
    assert 200 == res.status_code
    log.info("Oncology web connection status: %s", res.status_code)
    log.info("Testcase Ended")

@pytest.mark.p0
@pytest.mark.p4
def test_healthcheck_ready():
    """ automation testcase - Verify's that GET /ready or API connection ready , when valid JWT cookies token is provided """
    log.info("Testcase Started - Verify's that GET /ready or API connection ready , when valid JWT cookies token is provided")
    log.info("Checking Oncology web Connection Ready")
    res = onc_web_service_valid_token.get(endpoints.HEALTH_READY, get_default_headers())
    assert 200 == res.status_code, "READY status: %s" % res.status_code
    log.info("Oncology web connection is ready")
    log.info("Testcase Ended")

test_data = [patient_info[0]['humanNameFirst']]
@pytest.mark.p0
@pytest.mark.p4
@pytest.mark.parametrize("search_by", test_data)
def test_list_of_all_patients(search_by):
    """ automation testcase - Verify's that GET /api/v1/flatstore-patient/flatstore_patients?searchString={searchString}&start={start}&perPage={perPage}
     successful or API fetches all patients information list using search parameters, when valid JWT cookies token is provided """
    log.info("Testcase Started - Verify's that GET /api/v1/flatstore-patient/flatstore_patients?searchString={searchString}&start={start}&perPage={perPage} successful or API fetches all patients information list using search parameters, when valid JWT cookies token is provided")
    log.info("Searching chronicle patients using search string parameter with valid token")
    res = onc_web_service_valid_token.get(
        endpoints.CHRONICLE_PATIENTS.format(searchString=search_by, start=0, perPage=10), get_default_headers())
    assert 200 == res.status_code, "Chronicle Patients - List of Patient list status: %s" % res
    log.info("Searched chronicle patients list using search string parameter with valid token")
    log.info("Testcase Ended")

test_data = [patient_info[0]['humanNameFirst']]
@pytest.mark.p0
@pytest.mark.p4
@pytest.mark.parametrize("search_by", test_data)
@pytest.mark.skip(reason='TODO expired_token')
def test_list_of_all_patients_expired_token(search_by):
    """ automation testcase - Verify's that GET /api/v1/flatstore-patient/flatstore_patients?searchString={searchString}&start={start}&perPage={perPage}
        or API fails to fetches all patients information list using search parameters, when invalid JWT cookies token is provided """
    log.info("Testcase Started  - Verify's that GET /api/v1/flatstore-patient/flatstore_patients?searchString={searchString}&start={start}&perPage={perPage} or API fails to fetches all patients information list using search parameters, when invalid JWT cookies token is provided")
    log.info("Searching chronicle patients using search string parameter with expired token")
    res = onc_web_service_expired_token.get(
        endpoints.CHRONICLE_PATIENTS.format(searchString=search_by, start=0, perPage=10), get_default_headers())
    assert 401 == res.status_code, "Chronicle Patients - List of Patient list status: (expired token): %s" % res.status_code
    log.info("Getting Unauthorized Response")
    log.info("Testcase Ended")

test_data = [patient_info[0]['humanNameFirst']]
@pytest.mark.p0
@pytest.mark.p4
@pytest.mark.parametrize("search_by", test_data)
@pytest.mark.skip(reason='TODO empty_token')
def test_list_of_all_patients_empty_token(search_by):
    """ automation testcase - Verify's that GET /api/v1/flatstore-patient/flatstore_patients?searchString={searchString}&start={start}&perPage={perPage}
    or API fails to fetches all patients information list using search parameters, when empty JWT cookies token is provided """
    log.info("Testcase Started - Verify's that GET /api/v1/flatstore-patient/flatstore_patients?searchString={searchString}&start={start}&perPage={perPage} or API fails to fetches all patients information list using search parameters, when empty JWT cookies token is provided")
    log.info("Searching chronicle patients using search string parameter with empty token")
    res = onc_web_service_empty_token.get(
        endpoints.CHRONICLE_PATIENTS.format(searchString=search_by, start=0, perPage=10), get_default_headers())
    assert 401 == res.status_code, "Chronicle Patients - List of Patient list status: %s" % res.status_code
    log.info("Testcase Ended")

@pytest.mark.p0
def find_patient_from_patientList():
    """ Getting list of patient IDs using search string """
    res = onc_web_service_valid_token.get(endpoints.CHRONICLE_PATIENTS.format(searchString=patient_info[0]['humanNameFirst'], start=0, perPage=10),
                                          get_default_headers())
    assert 200 == res.status_code, "ROUTES status: %s" % res
    list_of_PatientIds = []
    patient_list = json.loads(res.text_payload)
    for k, v in patient_list.items():
        if k == 'matchingPatients':
            for idList in v:
                if '_id' in idList:
                    for kId, vId in idList.items():
                        if kId == '_id':
                            list_of_PatientIds.append(vId)
    return list_of_PatientIds[2]


test_data = [patient_info[0]['mrn']]
@pytest.mark.p0
@pytest.mark.p4
@pytest.mark.parametrize("mrn_value", test_data)
def test_prepopulation_patient(mrn_value):
    """ automation testcase - Verify's that GET /api/v1/flatstore-patient/patient_prepopulation/ or API fetches patient information for pre population given
    the patient ID, when valid JWT cookies token is provided """
    log.info("Testcase Started - Verify's that GET /api/v1/flatstore-patient/patient_prepopulation/ or API fetches patient information for pre population given the patient ID, when valid JWT cookies token is provided")
    log.info("Retrieve patient information for pre population for given patient ID")
    chronicle_patient_prepopulation = endpoints.CHRONICLE_PATIENT_PREPOPULATION
    endpoint_temp = chronicle_patient_prepopulation + find_patient_from_patientList()
    res = onc_web_service_valid_token.get(endpoint_temp, get_default_headers())
    assert 200 == res.status_code, "Retrieve patient information for pre population given the patient ID: %s" % res.status_code
    log.info("Retrieved patient information for pre population for given patient ID")
    verify_patient = json.loads(res.text_payload)
    log.info("Validating mrn values from retrieved patient data")
    for k, v in verify_patient.items():
        if k == 'mrn':
            assert v == mrn_value, "MRN not found for patient: %s" % mrn_value
    log.info("Testcase Ended")

@pytest.mark.p0
@pytest.mark.p4
@pytest.mark.skip(reason='TODO expired_token')
def test_prepopulation_patient_expired_token():
    """ automation testcase - Verify's that GET /api/v1/flatstore-patient/patient_prepopulation/ or API fails to fetches patient information for pre population given
        the patient ID, when invalid JWT cookies token is provided """
    log.info("Testcase Started - Verify's that GET /api/v1/flatstore-patient/patient_prepopulation/ or API fails to fetches patient information for pre population given the patient ID, when invalid JWT cookies token is provided")
    chronicle_patient_prepopulation = endpoints.CHRONICLE_PATIENT_PREPOPULATION
    endpoint_temp = chronicle_patient_prepopulation + find_patient_from_patientList()
    res = onc_web_service_expired_token.get(endpoint_temp, get_default_headers())
    assert 401 == res.status_code, "Retrieve patient information for pre population given the patient ID: %s" % res.status_code
    log.info("Testcase Ended")

@pytest.mark.p0
@pytest.mark.p4
@pytest.mark.skip(reason='TODO empty_token')
def test_prepopulation_patient_empty_token():
    """ automation testcase - Verify's that GET /api/v1/flatstore-patient/patient_prepopulation/ or API fails to fetches patient information for pre population given
            the patient ID, when empty JWT cookies token is provided """
    log.info("Testcase Started - Verify's that GET /api/v1/flatstore-patient/patient_prepopulation/ or API fails to fetches patient information for pre population given \
            the patient ID, when empty JWT cookies token is provided")
    chronicle_patient_prepopulation = endpoints.CHRONICLE_PATIENT_PREPOPULATION
    endpoint_temp = chronicle_patient_prepopulation + find_patient_from_patientList()
    res = onc_web_service_empty_token.get(endpoint_temp, get_default_headers())
    assert 401 == res.status_code, "Retrieve patient information for pre population given the patient ID: %s" % res
    log.info("Testcase Ended")
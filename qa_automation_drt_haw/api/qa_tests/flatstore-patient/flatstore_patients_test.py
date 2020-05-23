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
import re
import string
import json

"""Data_Generator Class -Generating string for patients search and string patient information to use in testcase methods"""
patient_info = Data_Generator('flatstore').patients_info

username = Config.portal_2_roles_username
psw = Config.portal_2_roles_password

flatstore_patient_info = ServiceInfo('flatstore-patient')
valid_jwt = Token(username, psw)

flatstore_patient_service_valid_token = Service(flatstore_patient_info.url, token=str(valid_jwt), sslcert=False)
flatstore_patient_service_empty_token = Service(flatstore_patient_info.url, token="", sslcert=False)
flatstore_patient_service_invalid_token = Service(flatstore_patient_info.url, token="948390hffh49", sslcert=False)
# TODO
flatstore_patient_service_expired_token = Service(flatstore_patient_info.url, token="expired", sslcert=False)

regex = re.compile('[@_!#$%^&*()<>?/|}{~:]')

@pytest.mark.p0
@pytest.mark.p4
def test_healthcheck_alive():
    """ automation testcase - Verify's that GET /v1/health/alive or API connection alive , when valid token is provided """
    log.info(
        "Testcase Started - Verify's that GET /v1/health/alive or API connection alive , when valid token is provided")
    log.info("Checking Flatstore service Connection Status")
    res = flatstore_patient_service_valid_token.get(endpoints.HEALTH_ALIVE, get_default_headers())
    assert 200 == res.status_code, "ALIVE status: %s" % res.status_code
    log.info("Flatstore service connection status: %s", res.status_code)
    log.info("Testcase Ended")


@pytest.mark.p0
@pytest.mark.p4
def test_healthcheck_ready():
    """ automation testcase - Verify's that GET /v1/health/ready or API connection ready , when valid token is provided """
    log.info(
        "Testcase Started - Verify's that GET /v1/health/ready or API connection ready , when valid token is provided")
    log.info("Checking Flatstore service Connection Ready")
    res = flatstore_patient_service_empty_token.get(endpoints.HEALTH_READY, get_default_headers())
    assert 200 == res.status_code, "READY status: %s" % res.status_code
    assert {'flat-store': True, 'postgres': True} == res.json_payload
    log.info("Flatstore service connection is ready")
    log.info("Testcase Ended")


@pytest.mark.p0
@pytest.mark.p4
def test_flatstore_patients_empty_token():
    """ automation testcase - Verify's that GET /v1/flatstore_patients or API fails fetches all patients information , when empty token is
    provided """
    log.info("Testcase Started - Verify's that GET /v1/flatstore_patients or API fails fetches all patients information , when empty token is \
            provided")
    log.info("Fetching all patients information using GET request with empty token")
    res = flatstore_patient_service_empty_token.get(endpoints.FLATSTORE_PATIENTS, get_default_headers())
    assert 401 == res.status_code, "CHRONICLE PATIENTS status: %s" % res.status_code
    log.info("Getting Unauthorized Response")
    log.info("Testcase Ended")


@pytest.mark.p0
@pytest.mark.p4
@pytest.mark.skip(reason='TODO expired_token')
def test_flatstore_patients_expired_token():
    """ automation testcase - Verify's that GET /v1/flatstore_patients or API fails fetches all patients information , when expired token is
    provided """
    log.info("Testcase Started - Verify's that GET /v1/flatstore_patients or API fails fetches all patients information , when expired token is \
    provided ")
    log.info("Fetching all patients information using GET request with expired token")
    res = flatstore_patient_service_expired_token.get(endpoints.FLATSTORE_PATIENTS, get_default_headers())
    assert 401 == res.status_code, "CHRONICLE PATIENTS status: %s" % res.status_code
    log.info("Getting Unauthorized Response")
    log.info("Testcase Ended")


@pytest.mark.p0
@pytest.mark.p4
def test_flatstore_patients_invalid_token():
    """ automation testcase - Verify's that GET /v1/flatstore_patients or API fails fetches all patients information , when invalid token is
    provided """
    log.info("Testcase Started - Verify's that GET /v1/flatstore_patients or API fails fetches all patients information , when invalid token is \
    provided ")
    log.info("Fetching all patients information using GET request with invalid token")
    res = flatstore_patient_service_invalid_token.get(endpoints.FLATSTORE_PATIENTS, get_default_headers())
    assert 401 == res.status_code, "CHRONICLE PATIENTS status: %s" % res.status_code
    log.info("Getting Unauthorized Response")
    log.info("Testcase Ended")


test_data = [patient_info[0]['humanNameFirst']]


@pytest.mark.p0
@pytest.mark.p4
@pytest.mark.parametrize("search_by", test_data)
def test_flatstore_patients_valid_token(search_by):
    """ automation testcase - Verify's that GET /v1/flatstore_patients successful or API fetches all patients information , when valid token is
        provided """
    log.info("Testcase Started - Verify's that GET /v1/flatstore_patients successful or API fetches all patients information , when valid token is \
        provided")
    log.info("Fetching all patients information using GET request with valid token")
    res = flatstore_patient_service_valid_token.get(endpoints.FLATSTORE_PATIENTS, get_default_headers(),
                                                    {'searchString': search_by, 'perPage': 10})
    assert 200 == res.status_code, "CHRONICLE PATIENTS status: %s" % res.status_code
    log.info("Fetched all patients information using GET request with valid token")
    log.info("Testcase Ended")


test_data = [patient_info[0]['humanNameFirst'] + patient_info[0]['humanNameLast']]


@pytest.mark.p0
@pytest.mark.p4
@pytest.mark.parametrize("patient_fullname", test_data)
def test_search_patient_by_full_name(patient_fullname):
    """ automation testcase - Verify's that GET /v1/flatstore_patients or API fetches all patients information by patients fullname
    provided in params , when valid token is provided """
    log.info("Testcase Started - Verify's that GET /v1/flatstore_patients or API fetches all patients information by patients fullname \
    provided in params , when valid token is provided")
    log.info(
        "Fetching all patients information using GET request with valid token and serachString params as patient fullname")
    res = flatstore_patient_service_valid_token.get(endpoints.FLATSTORE_PATIENTS, get_default_headers(),
                                                    {'searchString': patient_fullname, 'perPage': 20})
    assert 200 == res.status_code
    json_res = res.json_payload
    log.info(
        "Fetched all patient information using GET request with valid token and serachString params as patient fullname")
    if json_res['pageInfo']['total'] == 1:
        assert patient_fullname == json_res['matchingPatients'][0]['humanNameFirst'] + json_res['matchingPatients'][0][
            'humanNameLast']
        log.info(
            "Validated patient with fullname")
    log.info("Testcase Ended")


# TODO add more value for test_data = ["-=-=-=-=-=-", "-------","??????????","12334567890-","00-000-0000","SELECT * FROM Patient"] these value are failing due to 400 bad request and not allowing special characters
test_data = ["ioioii9", "000000", "iroei0", "Paris Syapse1", "       ", "0000000000"]


@pytest.mark.p0
@pytest.mark.p4
@pytest.mark.parametrize("patient_name", test_data)
def test_search_patient_name_mrn_not_exist(patient_name):
    """ Search patient who's mrn no doesn't exists"""
    log.info("Testcase Started - Search patient who's mrn no doesn't exists")
    log.info(
        "Fetching all patients information using GET request with valid token and searchString params who's mrn value doesn't exist")
    flatstore_patients = endpoints.FLATSTORE_PATIENTS
    endpoint_temp = flatstore_patients + '?searchString=%s' % patient_name
    res = flatstore_patient_service_valid_token.get(endpoint_temp, get_default_headers())
    assert 200 == res.status_code, "Status code: not 200"
    log.info(
        "Fetched all patient information using GET request with valid token and searchString params who's mrn value doesn't exist")
    json_res = res.json_payload
    assert 0 == json_res['pageInfo']['total'], "%s patient was found "
    log.info("Validated page total count")
    log.info("Testcase Ended")


test_data = [patient_info[0]['humanNameFirst']]


@pytest.mark.p0
@pytest.mark.p4
@pytest.mark.parametrize("patient_name", test_data)
def test_search_patient_partial_name_mrn(patient_name):
    """ automation testcase - Verify's that GET /v1/flatstore_patients or API fetches all patients information by patient's partial name
        provided in params who's mrn value is present, when valid token is provided """
    log.info("Testcase Started - Verify's that GET /v1/flatstore_patients or API fetches all patients information by patient's partial name \
        provided in params who's mrn value is present, when valid token is provided")
    log.info(
        "Fetching all patients information using GET request with valid token and searchString params as patient's partial name")
    res = flatstore_patient_service_valid_token.get(endpoints.FLATSTORE_PATIENTS, get_default_headers(),
                                                    {'searchString': patient_name, 'perPage': 20})
    assert 200 == res.status_code
    json_res = res.json_payload
    log.info(
        "Fetched all patients information using GET request with valid token and searchString params as patient's partial name")
    log.info("Validating patients with partial name")
    if json_res['pageInfo']['total'] > 0:
        for i in range(len(json_res['matchingPatients'])):
            patient_search_str = json_res['matchingPatients'][i]['humanNameFirst'] + " " + \
                                 json_res['matchingPatients'][i][
                                     'humanNameLast'] + json_res['matchingPatients'][i]['mrn']
            if patient_name.lower() not in patient_search_str.lower():
                assert False, "Search result is not correct for %s" % patient_name
    log.info("Validated patients with partial name")
    log.info("Testcase Ended")


test_data = [patient_info[0]['mrn']]


# TODO add pramas "patient_info" who's params value contains disallowed character
@pytest.mark.p0
@pytest.mark.p4
@pytest.mark.parametrize("mrn_no", test_data)
def test_search_patient_by_mrn(mrn_no):
    """ automation testcase - Verify's that GET /v1/flatstore_patients or API fetches all patients information by mrn value of patient
            provided in params , when valid token is provided """
    log.info("Testcase Started - Verify's that GET /v1/flatstore_patients or API fetches all patients information by mrn value of patient \
            provided in params , when valid token is provided")
    log.info(
        "Fetching all patients information using GET request with valid token and searchString params as patient's mrn_no")
    res = flatstore_patient_service_valid_token.get(endpoints.FLATSTORE_PATIENTS, get_default_headers(),
                                                    {'searchString': mrn_no, 'perPage': 20})
    assert 200 == res.status_code
    json_res = res.json_payload
    log.info(
        "Fetched all patients information using GET request with valid token and searchString params as patient's mrn_no"
    )
    log.info("Validating patient with mrn no value")
    if json_res['pageInfo']['total'] > 0:
        for i in range(len(json_res['matchingPatients'])):
            assert json_res['matchingPatients'][i]['mrn'] == mrn_no
    log.info("Validated patient with mrn no value")
    log.info("Testcase Ended")

test_data = ["-1", "2", "100", "1000", "5000"]  # 0?
patient_data = [patient_info[0]['mrn']]


@pytest.mark.p0
@pytest.mark.p4
@pytest.mark.parametrize("num_pages", test_data)
@pytest.mark.parametrize("patient_name", patient_data)
def test_pagination(num_pages, patient_name):
    """ automation testcase - Verify's that GET /v1/flatstore_patients or API fetches all patients information details providing number of pages,
     when valid token is provided """
    log.info("Testcase Started - Verify's that GET /v1/flatstore_patients or API fetches all patients information details providing number of pages, \
     when valid token is provided")
    log.info(
        "Fetching all patients information using GET request with valid token and searchString, perPage result params")
    res = flatstore_patient_service_valid_token.get(endpoints.FLATSTORE_PATIENTS, get_default_headers(),
                                                    {'searchString': patient_name, 'perPage': num_pages})
    assert 200 == res.status_code
    json_res = res.json_payload
    log.info(
        "Fetched all patients information using GET request with valid token and searchString, perPage result params")
    log.info(" Validating perPage patients results count")
    if json_res['pageInfo']['total'] > 0:
        res_pages = json_res['pageInfo']['nPages']
        res_per_page = json_res['pageInfo']['perPage']
        res_total = json_res['pageInfo']['total']

        pages = res_total // res_per_page + (1 if res_total % res_per_page > 0 else 0)
        assert pages == res_pages
        log.info("Validated perPage patients results count")
    log.info("Testcase Ended")

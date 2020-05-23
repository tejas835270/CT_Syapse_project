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
patient_name = pytest.data.get_mtb_create_case_data('patient_name')
unacceptable_special_chars = pytest.data.get_mtb_create_case_data('Special_chars')
error_message='The field must not contain the following special characters: ~ ` @ # $ ^ { } |'

@pytest.mark.p0
@pytest.mark.p4
@pytest.mark.parametrize("search_by", unacceptable_special_chars)
def test_error_message_for_unacceptable_special_chars(search_by):
    pytest.log_test = "Verify error message response appears when special characters like (~`@#$^{}|) are entered in searchString parameter of flatstore_patients endpoint"
    pytest.log_link = ['https://syapse.atlassian.net/browse/BUMP-633']
    log.info("Test Started- to Verify error message response appears when special characters like (~`@#$^{}|) are entered in searchString parameter of flatstore_patients endpoint")

    Patient_name= patient_name + search_by
    log.info("Try to search the patient by '%s'" % Patient_name)
    res = flatstore_patient_service_valid_token.get(endpoints.FLATSTORE_PATIENTS, get_default_headers(),{'searchString': Patient_name, 'perPage': 10})

    log.info("Verify the status code response gives 400")
    if res.status_code == 400:
        log.info("status code is valid i.e'%s' " % res.status_code)
    else:
        log.error("status code is invalid i.e'%s' " % res.status_code)
        assert False,"status code is invalid i.e'%s' " % res.status_code

    log.info("Verify the json response gives valid error message")
    json_res = res.json_payload

    if json_res == error_message :
        log.info("Response contains valid error message '%s'" % json_res)
        assert True,"Response  does not contain error message '%s'" % json_res
    else:
        log.error("Response  does not contain error message '%s'" % json_res)
        assert False

acceptable_special_chars = pytest.data.get_mtb_create_case_data('acceptable_special_chars')
@pytest.mark.p0
@pytest.mark.p4
@pytest.mark.parametrize("search_by", acceptable_special_chars)
def test_no_error_message_for_acceptable_special_chars(search_by):
    pytest.log_test = "Verify no error message response appears when special characters like ('-) are entered in searchString parameter of flatstore_patients endpoint"
    pytest.log_link = ['https://syapse.atlassian.net/browse/BUMP-633']
    log.info("Test Started- to Verify no error message response appears when special characters like ('-) are entered in searchString parameter of flatstore_patients endpoint")

    Patient_name= patient_name + search_by
    log.info("Try to search the patient by '%s'" %Patient_name)
    res = flatstore_patient_service_valid_token.get(endpoints.FLATSTORE_PATIENTS, get_default_headers(),{'searchString': Patient_name, 'perPage': 10})

    log.info("Verify the status code response gives 200")
    if res.status_code == 200:
        log.info("status code is valid i.e'%s' " %res.status_code)
    else:
        log.error("status code is invalid i.e'%s' " % res.status_code)
        assert False, "status code is invalid i.e'%s' " % res.status_code

    log.info("Verify the json response does not give error message for acceptable special chars ('-)")
    json_res = res.json_payload

    if error_message in json_res:
        log.error("Response contains the error message '%s'" % json_res)
        assert False
    else:
        log.info("Response  does not contain error message '%s'" % json_res)
        assert True, "Response contains error message '%s'" % json_res

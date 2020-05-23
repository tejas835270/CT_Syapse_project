import pytest
from qa_automation_drt_haw.api.api_utils.serviceApi import ServiceInfo, Token
from qa_automation_core.api.service import Service
from qa_automation_core.api.api_headers import get_default_headers
import json
import base64
import string
import re
from qa_automation_drt_haw.ui.ui_utils.Logs import log
from qa_automation_drt_haw.settings import Config
from qa_automation_drt_haw.api.qa_test_data.urls import Mtb_Endpoints, Flatstore_Endpoints, Oncology_Endpoints

username = Config.portal_2_roles_username
psw = Config.portal_2_roles_password
valid_jwt = Token(username, psw)

regex = re.compile('[@_!#$%^&*()<>?/|}{~:]')

""" Get patients information by generating different string combination"""


def get_patients(service):
    try:
        for k in list(string.ascii_lowercase):
            for j in list(string.ascii_lowercase):
                x = k + j  # x is string value e.g('aa', 'ab' .........'za', 'zb'...'zz')
                log.info("Constructed string to provide in searchString parameter: %s", x)
                log.info("Requesting MTB Service endpoint to fetch patient detail by providing: %s", x)

                if service == 'mtb':
                    patient_info = get_mtb(x)  # Gets patients information from mtb endpoint
                elif service == "flatstore" or service == 'pre-population' or service == 'oncology':
                    patient_info = get_flatstore_and_oncology(x,
                                                              service)  # Gets patients information from flatstore and chronicle endpoint
                if len(patient_info) > 1:
                    break
            else:
                print("Patient %s has not been found , please try another string" % x)
                continue
            break
    except ValueError:
        print("Patients has not not been found, please try another string")
    return patient_info


def get_mtb(x):
    """ String value x passes in GET_MTB_PATIENTS endpoints parameter"""
    mtb_info = ServiceInfo('mtb-web')
    mtb_web_service_valid_token = Service(mtb_info.url, jwt_cookie=str(Token(username, psw)),
                                          sslcert=False)
    res = mtb_web_service_valid_token.get(Mtb_Endpoints.GET_MTB_PATIENTS, get_default_headers(),
                                          {'searchString': x, 'perPage': 10})
    assert 200 == res.status_code
    json_res = json.loads(res.text_payload)
    patient_info = []
    # Requests response are store patient_info variable using loop on response
    if json_res['pageInfo']['total'] > 1:
        for i in json_res['matchingPatients']:
            if (regex.search(str(i['mrn'])) is None) and str(i['mrn']) is not None:
                patient_data = {'humanNameFirst': i['humanNameFirst'],
                                'humanNameLast': i['humanNameLast'],
                                'humanNameMiddle': i['humanNameMiddle'], 'mrn': i['mrn'], 'name': i['name'], 'patientId': i['_id'],
                                'dob': i['dob']}
                patient_info.append(patient_data)
    return patient_info


def get_flatstore_and_oncology(x, service):
    flatstore_patient_info = ServiceInfo('flatstore-patient')
    flatstore_patient_service_valid_token = Service(flatstore_patient_info.url, token=str(valid_jwt),
                                                    sslcert=False)
    res = flatstore_patient_service_valid_token.get(Flatstore_Endpoints.FLATSTORE_PATIENTS,
                                                    get_default_headers(),
                                                    {'searchString': x, 'perPage': 20})
    assert 200 == res.status_code
    json_res = res.json_payload
    if service == 'pre-population':
        patient_info = json_res['matchingPatients'][0]['patientId']
    else:
        patient_info = []
    # Requests response are store patient_info variable using loop on response
    # Storing value for flatstore and oncology both services
    if service == 'flatstore' or service == 'oncology':
        for i in json_res['matchingPatients']:
            if (regex.search(str(i['mrn'])) is None) and str(i['mrn']) is not None:
                patient_data = {'humanNameFirst': i['humanNameFirst'],
                                'humanNameLast': i['humanNameLast'],
                                'humanNameMiddle': i['humanNameMiddle'],
                                'mrn': i['mrn'], 'name': i['name'], 'patientId': i['patientId'],
                                'dob': i['dob']}
                patient_info.append(patient_data)
    return patient_info


class Data_Generator:

    def __init__(self, service):
        self.patients_info = get_patients(service)

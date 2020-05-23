# TODO - Chronicle pod is down now, below code is not require for a timing.
# from datetime import datetime
# from qa_automation_drt_haw.settings import Config
# import pytest
# from qa_automation_drt_haw.api.api_utils.serviceApi import ServiceAPI, ServiceInfo, Token
# from qa_automation_core.api.service import Service
# from qa_automation_core.api.api_headers import (get_default_headers,
#                                                 post_default_headers, post_headers_content_json_accept_text)
# from endpoints_chronicle import endpoints
# from qa_automation_drt_haw.ui.ui_utils.Logs import log
# import json
#
# username = Config.portal_2_roles_username
# psw = Config.portal_2_roles_password
#
#
# chronicle_service_info = ServiceInfo('chronicle-service')
# oncology_info = ServiceInfo('oncology-web')
#
# valid_jwt = Token(username, psw)
#
# chronicle_service_valid_token = Service(chronicle_service_info.url, jwt_cookie=str(valid_jwt), sslcert=False)
# chronicle_service_empty_token = Service(chronicle_service_info.url, token="", sslcert=False)
# chronicle_service_invalid_token = Service(chronicle_service_info.url, token="948390hffh49", sslcert=False)
#
# chronicle_service_expired_token = Service(chronicle_service_info.url, token="expired", sslcert=False)
# onc_web_service_valid_token = Service(oncology_info.url, jwt_cookie=str(valid_jwt), sslcert=False)
#
#
# @pytest.mark.p0
# def test_chronicle_healthcheck_alive():
#     """ automation testcase - Verify's that GET /v1/health/alive or API connection alive , when valid JWT cookies token is provided """
#     log.info("Testcase Started - Verify's that GET /v1/health/alive or API connection alive , when valid JWT cookies token is provided")
#     log.info("Checking Chronicle service Connection Status")
#     res = chronicle_service_valid_token.get(endpoints.HEALTH_ALIVE, get_default_headers())
#     assert 200 == res.status_code, "ALIVE status: %s" % res.status_code
#     log.info("Chronicle service connection status: %s", res.status_code)
#     log.info("Testcase Ended")
#
# @pytest.mark.p0
# def test_chronicle_healthcheck_ready():
#     """ automation testcase - Verify's that GET /v1/health/ready or API connection ready , when valid JWT cookies token is provided """
#     log.info("Testcase Started - Verify's that GET /v1/health/ready or API connection ready , when valid JWT cookies token is provided")
#     log.info("Checking Chronicle service Connection Ready")
#     res = chronicle_service_valid_token.get(endpoints.HEALTH_READY, get_default_headers())
#     assert 200 == res.status_code, "ALIVE status: %s" % res.status_code
#     log.info("Chronicle service connection is ready")
#     log.info("Testcase Ended")

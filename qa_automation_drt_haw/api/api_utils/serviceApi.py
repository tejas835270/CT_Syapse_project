import json
import os
import pytest
import requests
from qa_automation_drt_haw.settings import Config


class Token():
    GRANT_TYPE = 'password'
    SCOPE = 'openid email profile'

    # Config code added to fetch Oauth client id and client secret key details
    if pytest.env == 'dev':
        AUTH0_URL = 'https://dev-syapse.auth0.com/oauth/token'
        CENTRAL_AUTHZ_URL = 'https://ambassador.dev.syapse.com/authz/v1/token/swap?input_token='
        CLIENT_ID = Config.auth_client_id
        CLIENT_SECRET = Config.auth_client_secret
    elif pytest.env == 'sqa':
        AUTH0_URL = 'https://syapse.auth0.com/oauth/token'
        CENTRAL_AUTHZ_URL = 'https://ambassador-sqa.syapse.com/authz/v1/token/swap?input_token='
        CLIENT_ID = Config.auth_client_id
        CLIENT_SECRET = Config.auth_client_secret

    def __init__(self, username, password):
        self.sess = requests.session()
        auth0_token = self.get_auth0_token(username, password)
        self.token = self.get_verified_token(auth0_token)

    def __str__(self):
        return str(self.token)

    def get_auth0_token(self, username, password):
        auth0_body = {
            "grant_type": self.GRANT_TYPE,
            "username": username,
            "password": password,
            "scope": self.SCOPE,
            "client_id": self.CLIENT_ID,
            "client_secret": self.CLIENT_SECRET
        }
        res = self.sess.post(self.AUTH0_URL, auth0_body)
        return res.json()['id_token']

    def get_verified_token(self, auth0_token):
        res = self.sess.get(self.CENTRAL_AUTHZ_URL + auth0_token)
        if res.status_code == 200 and "token" in res.text:
            return str(json.loads(res.text).get("token"))
        else:
            return "-"


class ServiceInfo():
    modeLocal = False if os.environ.get('JENKINS_URL') else True

    def __init__(self, service):

        self.expired_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJodHRwczovL2NlbnRyYWwtYXV0aHouZGV2LnN5YXBzZS5jb20iLCJzdWIiOiIyMDE5LTA2LTIxIDE4OjM2OjI5LjI5NzcxN0BodHRwczovL2NlbnRyYWwtYXV0aHouZGV2LnN5YXBzZS5jb20iLCJhdWQiOlsiY2xpbmljYWwtdHJpYWxzIiwicGF0aWVudC1maW5kZXIiLCJwYXRpZW50LWNvbnRleHQiLCJ1cmwtYXV0aGVudGljYXRvciIsIm1keC1zZXJ2aWNlIiwibXRiLXNlcnZpY2UiLCJzeWFwc2UtYXBwcyIsImV4cGxvcmVyIiwiY2Fib29zZSIsImRhdGEtdmFsaWRhdGlvbi13b3JrZmxvdyIsImNlbnRyYWwtYXV0aHoiXSwiZXhwIjoxNTYxMTQ1Nzg5LCJpYXQiOjE1NjExNDIxODksInR5cGUiOiJhY2Nlc3MiLCJjdXN0b20iOnsiY2xpbmljYWxfZGF0YV9wcm9qZWN0IjoiIiwidXNlcl9pZCI6IjEwMCIsIndyaXRlX3Byb2plY3RzIjpbXSwiZ3VpZCI6IiIsImN1c3RvbWVyIjoiIiwicm9sZXMiOlt7Im5hbWUiOiJjaHJvbmljbGUgZWRpdG9yIiwiaWQiOjJ9LHsibmFtZSI6Im1vbGVjdWxhciBUdW1vciBib2FyZCBjb29yZGluYXRvciIsImlkIjozfV0sImhvc3RuYW1lIjoiaW50ZWdyYXRpb24xLmRldiIsInN1Ym9yZ3MiOltdLCJyZWFkX3Byb2plY3RzIjpbXSwib3JnYW5pemF0aW9uIjoiUG9ydGFsIFRlc3QgT3JnIiwidXNlcl9mdWxsX25hbWUiOiJBUEkgU3lhcHNlIiwiZW1haWwiOiJzeWFwc2VtYWluK2FwaUBnbWFpbC5jb20ifSwianRpIjoiOWJkZGQwZmU5NmE2NGMzYmJhYWQwOTgxNzRkYTg0YzAifQ.ObKMzcnr6lCct85IF9m-VXj_jzRP57BGQPKX3y_eToGjRH-IpiV4inQmexOHpU1-WMdQyI56cD6EdQru9MUhvmd0bPRca3ovn7RsCE6H_FC1qGWzE9Rg4mZQv7sR2iY1LVSdcmbbQAAvwYrv3_rnQ3kH94rJiXvDE4V3MjBGG9TiSFLJDfXfMcPkAMpYkQvX3ZBk9Z8a5L1LDSJPWWmWZ1QKstwjKlzD7JUIEVILqqoReZ2Rdg8BQKVftaOsL96u1ZZayWfaob1rL_rItfW-mPEWMom1WpityhEfdB_gjQxz5hf06bmGDfHwxCX7HAuD35-i-14UAP-nAFlaYRnLYw'

        if service == 'portal-web':
            # SQA env url format with -(hyphen) key
            if pytest.env == 'sqa':
                self.url = "https://portal-%s.syapse.com" % pytest.env
            else:
                self.url = "https://portal.%s.syapse.com" % pytest.env

        elif service == 'routing-service':
            if pytest.env == 'sqa':
                self.url = "https://routing-service-%s.svc.cluster.local" % pytest.env
            else:
                self.url = "https://routing-service.%s.svc.cluster.local" % pytest.env

            if self.modeLocal:
                self.url = "https://localhost:4000"

        elif service == 'oncology-web':
            if pytest.env == 'sqa':
                self.url = "https://oncology-%s.syapse.com" % pytest.env
            else:
                self.url = "https://oncology.%s.syapse.com" % pytest.env

        elif service == 'flatstore-patient':
            if pytest.env == 'sqa':
                self.url = "https://flatstore-patient-%s.svc.cluster.local" % pytest.env
            else:
                self.url = "https://flatstore-patient.%s.svc.cluster.local" % pytest.env

            if self.modeLocal:
                self.url = "https://localhost:8445"

        elif service == 'mtb-web':
            if pytest.env == 'sqa':
                self.url = "https://mtb-%s.syapse.com" % pytest.env
            else:
                self.url = "https://mtb.%s.syapse.com" % pytest.env

        elif service == 'chronicle-service':
            if pytest.env == 'sqa':
                self.url = "https://chronicle-service-%s.svc.cluster.local" % pytest.env
            else:
                self.url = "https://chronicle-service.%s.svc.cluster.local" % pytest.env

            if self.modeLocal:
                self.url = "https://localhost:8446"

        elif service == 'minerva-service':
            if pytest.env == 'sqa':
                self.url = "https://minerva-service-%s.svc.cluster.local" % pytest.env
            else:
                self.url = "https://minerva-service.%s.svc.cluster.local" % pytest.env

                if self.modeLocal:
                    self.url = "https://localhost:4001"

        elif service == 'file-service':
            if pytest.env == 'sqa':
                self.url = "https://file-service-%s.svc.cluster.local" % pytest.env
            else:
                self.url = "https://file-service.%s.svc.cluster.local" % pytest.env

                if self.modeLocal:
                    self.url = "https://localhost:5001"

class ServiceAPI():

    def __init__(self, username, password, service_name, token_type='valid'):
        self.service_info = ServiceInfo(service_name)
        self.base_url = self.service_info.url
        self.sess = requests.session()
        if token_type == 'valid':
            self.token = str(Token(username, password))
            self.headers = {'Authorization': 'Bearer ' + self.token}
        elif token_type == 'invalid':
            self.token = "00" + str(Token(username, password))[2:]
            self.headers = {'Authorization': 'Bearer ' + self.token}
        elif token_type == 'expired':
            self.token = self.service_info.expired_token
            self.headers = {'Authorization': 'Bearer ' + self.service_info.expired_token}
        elif token_type == 'empty':
            self.token = ''
            self.headers = {'Authorization': ''}

        self.token_type = token_type

    def endpoint(self, path, overwrite=True):
        if overwrite:
            return self.base_url + self.service_info.endpoints[path]
        else:
            return self.base_url + path

    def get(self, endpoint, headers=None, overwrite=True):

        if not headers:
            headers = self.headers
        else:
            headers.update(self.headers)
        endpoint = self.endpoint(endpoint, overwrite)
        response = self.sess.get(endpoint, headers=headers, verify=False)
        resp = dict()
        resp['status_code'] = response.status_code
        resp['body'] = response
        return resp

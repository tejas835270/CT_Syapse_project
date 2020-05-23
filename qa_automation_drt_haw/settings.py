""" Application configuration. """

import os
from decouple import config
import pytest

# adding below if-else condition because the path to import "decrypt and DataJson classes" are different for local and docker ex
if os.getenv('TYPE') is None:
    from qa_automation_drt_haw.qa_utils.encrypt_decrypt import decrypt
    from qa_automation_drt_haw.ui.ui_utils.Data_tricks import DataJson
else:
    from qa_utils.encrypt_decrypt import decrypt
    from ui.ui_utils.Data_tricks import DataJson

pytest.data = DataJson()


class Config(object):
    """Config

    The configuration for the application. Each configuration option is specified as a class
    constant with a value derived from the environment using the :meth:`decouple.config` function.

    Default values, when specified, should be production-safe. If a production-safe value is
    dependent on usage, a default is not specified and is instead expected to be configured by
    the environment.
    """

    ##
    #: The `APP_DIR` endpoints to the location of the Flask app on the local
    #: filesystem.
    #:
    #: This value is not configurable as it derives itself from the path of this
    #: settings file, as it is assumed to be in the `APP_DIR`.
    #:
    APP_DIR = os.path.abspath(os.path.dirname(__file__))

    ##
    #: The `PROJECT_ROOT` specifies the path to the project (the directory
    #: containing migrations, tests, configurations, etc).
    #:
    #: This value is not configurable as it derives itself from the parent
    #: directory of the `APP_DIR`.
    #:
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))

    ##
    #: The `ENV` specifies the environment context that the application is
    #: being run in (local, development, staging, production).
    #:
    #: In general it is considered bad practice to write code that depends on
    #: this value: the application should be unaware of its environment context.
    #:
    #: However, this value may be used to restrict or prevent certain actions
    #: based on context. For example, disabling dangerous or destructive
    #: administrative actions in a production environment.
    #:
    #: Default: `production`
    #:
    env: str = config('ENV', 'dev')

    # below variable stores priorities of testcases
    ui_dev: str = config('ui-dev', ["p0", "p1", "p2", "p3"])
    ui_sqa: str = config('ui-sqa', 'p4')

    # Access password for credentials for different environment
    dev_credential_password: str = config('CREDENTIALS_DEV', '')
    sqa_credential_password: str = config('CREDENTIALS_SQA', '')

    if os.environ['ENV'] == 'dev':
        # Credentials for dev

        # User having roles for only 2 tiles
        portal_2_roles_username: str = config('', pytest.data.get_user('portal_2_roles')['username'])
        portal_2_roles_password: str = config('', decrypt(pytest.data.get_user('portal_2_roles')['password'],
                                                          dev_credential_password))

        # User having access to chronicle
        portal_chronicle_username: str = config('', pytest.data.get_user('portal_chronicle')['username'])
        portal_chronicle_password: str = config('', decrypt(pytest.data.get_user('portal_chronicle')['password'],
                                                            dev_credential_password))

        # User having no roles to any tile
        portal_no_roles_username: str = config('', pytest.data.get_user('portal_no_roles')['username'])
        portal_no_roles_password: str = config('', decrypt(pytest.data.get_user('portal_no_roles')['password'],
                                                           dev_credential_password))

        # User used for mtb-web testing
        mtb_testing_only_username: str = config('', pytest.data.get_user('mtb_testing_only')['username'])
        mtb_testing_only_password: str = config('', decrypt(pytest.data.get_user('mtb_testing_only')['password'],
                                                            dev_credential_password))

        # User used for Tableau executive
        tableau_executive_only_username: str = config('', pytest.data.get_user('tableau_executive_only')['username'])
        tableau_executive_only_password: str = config('', decrypt(
            pytest.data.get_user('tableau_executive_only')['password'], dev_credential_password))

        # Oauth details for API Token
        auth_client_id: str = config('', pytest.data.get_user('api_auth_details')['client_id'])
        auth_client_secret: str = config('', pytest.data.get_user('api_auth_details')['client_secret'])

        # caseId from different organization
        integration2: str = config('', pytest.data.get_json_val('users_dev', 'org_cases', 'integration2'))

        # case with available attachments
        case_url_with_attachments = config('',pytest.data.get_json_val('dev','case_with_attachments','case_url'))

        # Patient MRN with reports associated with it
        auto_report_patient_mrn = config('',pytest.data.get_json_val('dev','auto_report_patient_mrn'))

        # Patient name having multiple search results
        patient_search_multiple_results = config('',pytest.data.get_json_val('dev','patient_search'))

        # Get File Token For Integration2.dev org
        integration2_file_token: str = config('', pytest.data.get_json_val('users_dev', 'org_token', 'integration2_file_token'))

        # DB credential details for minerva service
        minerva_db_host: str = config('', pytest.data.get_json_val('dev_db_conn','minerva','host'))
        minerva_db_user: str = config('', pytest.data.get_json_val('dev_db_conn','minerva','user'))
        minerva_db_password: str = config('', decrypt(pytest.data.get_json_val('dev_db_conn','minerva','password'),dev_credential_password))
        minerva_db_dbname: str = config('', pytest.data.get_json_val('dev_db_conn','minerva','database'))
        minerva_db_port: str = config('', pytest.data.get_json_val('dev_db_conn','minerva','port'))

        # DB credential details for flatstore service
        flatstore_db_host: str = config('', pytest.data.get_json_val('dev_db_conn', 'flatstore', 'host'))
        flatstore_db_user: str = config('', pytest.data.get_json_val('dev_db_conn', 'flatstore', 'user'))
        flatstore_db_password: str = config('', decrypt(pytest.data.get_json_val('dev_db_conn', 'flatstore', 'password'),dev_credential_password))
        flatstore_db_dbname: str = config('', pytest.data.get_json_val('dev_db_conn', 'flatstore', 'database'))
        flatstore_db_port: str = config('', pytest.data.get_json_val('dev_db_conn', 'flatstore', 'port'))

        # DB credential details for mdx service
        mdx_db_host: str = config('', pytest.data.get_json_val('dev_db_conn', 'mdx_service', 'host'))
        mdx_db_user: str = config('', pytest.data.get_json_val('dev_db_conn', 'mdx_service', 'user'))
        mdx_db_password: str = config('', decrypt(pytest.data.get_json_val('dev_db_conn', 'mdx_service', 'password'),dev_credential_password))
        mdx_db_dbname: str = config('', pytest.data.get_json_val('dev_db_conn', 'mdx_service', 'database'))
        mdx_db_port: str = config('', pytest.data.get_json_val('dev_db_conn', 'mdx_service', 'port'))

    elif os.environ['ENV'] == 'sqa':
        # Credentials for sqa

        # User having roles for only 2 tiles
        portal_2_roles_username: str = config('', pytest.data.get_json_val('users_sqa', 'portal_2_roles', 'username'))
        portal_2_roles_password: str = config('', decrypt(
            pytest.data.get_json_val('users_sqa', 'portal_2_roles', 'password'), sqa_credential_password))

        # User having access to chronicle
        portal_chronicle_username: str = config('',
                                                pytest.data.get_json_val('users_sqa', 'portal_chronicle', 'username'))
        portal_chronicle_password: str = config('', decrypt(
            pytest.data.get_json_val('users_sqa', 'portal_chronicle', 'password'), sqa_credential_password))

        # User having no roles to any tile
        portal_no_roles_username: str = config('', pytest.data.get_json_val('users_sqa', 'portal_no_roles', 'username'))
        portal_no_roles_password: str = config('', decrypt(
            pytest.data.get_json_val('users_sqa', 'portal_no_roles', 'password'), sqa_credential_password))

        # User used for mtb-web testing
        mtb_testing_only_username: str = config('',
                                                pytest.data.get_json_val('users_sqa', 'portal_no_roles', 'username'))
        mtb_testing_only_password: str = config('', decrypt(
            pytest.data.get_json_val('users_sqa', 'portal_no_roles', 'password'), sqa_credential_password))

        # User for 'CHI' organisation
        tableau_chi_username: str = config('', pytest.data.get_json_val('users_sqa', 'tableau_chi', 'username'))
        tableau_chi_password: str = config('', decrypt(pytest.data.get_json_val('users_sqa', 'tableau_chi', 'password'),
                                                       sqa_credential_password))

        # User for 'HFHS' organisation
        tableau_hfhs_username: str = config('', pytest.data.get_json_val('users_sqa', 'tableau_hfhs', 'username'))
        tableau_hfhs_password: str = config('',
                                            decrypt(pytest.data.get_json_val('users_sqa', 'tableau_hfhs', 'password'),
                                                    sqa_credential_password))

        # User for 'PMA' organisation
        tableau_pma_username: str = config('', pytest.data.get_json_val('users_sqa', 'tableau_pma', 'username'))
        tableau_pma_password: str = config('', decrypt(pytest.data.get_json_val('users_sqa', 'tableau_pma', 'password'),
                                                       sqa_credential_password))

        # User for 'AURORA' organisation
        tableau_aurora_username: str = config('', pytest.data.get_json_val('users_sqa', 'tableau_aurora', 'username'))
        tableau_aurora_password: str = config('', decrypt(
            pytest.data.get_json_val('users_sqa', 'tableau_aurora', 'password'), sqa_credential_password))

        # User for Tableau executive
        tableau_executive_only_username: str = config('',
                                                      pytest.data.get_json_val('users_sqa', 'tableau_executive_only',
                                                                               'username'))
        tableau_executive_only_password: str = config('', decrypt(
            pytest.data.get_json_val('users_sqa', 'tableau_executive_only', 'password'), sqa_credential_password))

        # User for PSJH
        PSJH_username: str = config('', pytest.data.get_json_val('users_sqa', 'PSJH', 'username'))
        PSJH_password: str = config('', decrypt(pytest.data.get_json_val('users_sqa', 'PSJH', 'password'),
                                                sqa_credential_password))

        # User for CHI_H
        CHI_H_username: str = config('', pytest.data.get_json_val('users_sqa', 'CHI_H', 'username'))
        CHI_H_password: str = config('', decrypt(pytest.data.get_json_val('users_sqa', 'CHI_H', 'password'),
                                                 sqa_credential_password))

        # User for CHI_F
        CHI_F_username: str = config('', pytest.data.get_json_val('users_sqa', 'CHI_F', 'username'))
        CHI_F_password: str = config('', decrypt(pytest.data.get_json_val('users_sqa', 'CHI_F', 'password'),
                                                 sqa_credential_password))

        # caseId from different organization
        integration2: str = config('', pytest.data.get_json_val('users_sqa', 'org_cases', 'integration2'))

        # OAuth details for API Token
        auth_client_id: str = config('', pytest.data.get_json_val('users_sqa', 'api_auth_details', 'client_id'))
        auth_client_secret: str = config('', decrypt(
            pytest.data.get_json_val('users_sqa', 'api_auth_details', 'client_secret'), sqa_credential_password))

        # case with available attachments
        case_url_with_attachments = config('', pytest.data.get_json_val('sqa', 'case_with_attachments', 'case_url'))

        # Patient MRN with reports associated with it
        auto_report_patient_mrn = config('', pytest.data.get_json_val('sqa', 'auto_report_patient_mrn'))

        # Patient name having multiple search results
        patient_search_multiple_results = config('', pytest.data.get_json_val('sqa', 'patient_search'))

        # Get File Token For Integration2.dev org
        integration2_file_token: str = config('', pytest.data.get_json_val('users_sqa', 'org_token', 'integration2_file_token'))

        # DB credential details for minerva service
        minerva_db_host: str = config('', pytest.data.get_json_val('sqa_db_conn', 'minerva', 'host'))
        minerva_db_user: str = config('', pytest.data.get_json_val('sqa_db_conn', 'minerva', 'user'))
        minerva_db_password: str = config('', decrypt(pytest.data.get_json_val('sqa_db_conn', 'minerva', 'password'),
                                                      sqa_credential_password))
        minerva_db_dbname: str = config('', pytest.data.get_json_val('sqa_db_conn', 'minerva', 'database'))
        minerva_db_port: str = config('', pytest.data.get_json_val('sqa_db_conn', 'minerva', 'port'))

        # DB credential details for flatstore service
        flatstore_db_host: str = config('', pytest.data.get_json_val('sqa_db_conn', 'flatstore', 'host'))
        flatstore_db_user: str = config('', pytest.data.get_json_val('sqa_db_conn', 'flatstore', 'user'))
        flatstore_db_password: str = config('',
                                            decrypt(pytest.data.get_json_val('sqa_db_conn', 'flatstore', 'password'),
                                                    sqa_credential_password))
        flatstore_db_dbname: str = config('', pytest.data.get_json_val('sqa_db_conn', 'flatstore', 'database'))
        flatstore_db_port: str = config('', pytest.data.get_json_val('sqa_db_conn', 'flatstore', 'port'))

        # DB credential details for mdx service
        mdx_db_host: str = config('', pytest.data.get_json_val('sqa_db_conn', 'mdx_service', 'host'))
        mdx_db_user: str = config('', pytest.data.get_json_val('sqa_db_conn', 'mdx_service', 'user'))
        mdx_db_password: str = config('', decrypt(pytest.data.get_json_val('sqa_db_conn', 'mdx_service', 'password'),
                                                  sqa_credential_password))
        mdx_db_dbname: str = config('', pytest.data.get_json_val('sqa_db_conn', 'mdx_service', 'database'))
        mdx_db_port: str = config('', pytest.data.get_json_val('sqa_db_conn', 'mdx_service', 'port'))

    API_PROTOCOL = config('API_PROTOCOL', "https")

import pytest
import time
from qa_automation_drt_haw.settings import Config
from qa_automation_drt_haw.qa_utils import backend_data as DB
from qa_automation_drt_haw.ui.ui_utils.Logs import log

username = Config.mtb_testing_only_username
psw = Config.mtb_testing_only_password



# todo: text will be changed
@pytest.fixture(scope="function")
def test_launch_mtb(app_test):
    log.info("Opening application")
    app_test.portal.login(username, psw)
    app_test.portal.navigate_to_mtb_service()

@pytest.mark.p0
@pytest.mark.p4
def test_db_flatstore():
    record_id = DB.get_patient_results_for_organisation()
    log.info(record_id)

@pytest.mark.p0
@pytest.mark.p4
def test_db_minerva():
    query = "Select * from mtb_Case"
    result = DB.query_db(db_name='minerva',query=query)
    log.info(result)






























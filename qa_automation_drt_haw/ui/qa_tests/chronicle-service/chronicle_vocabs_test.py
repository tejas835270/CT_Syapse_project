import pytest
import time
from qa_automation_drt_haw.settings import Config

from qa_automation_drt_haw.ui.ui_utils.Logs import log

username = Config.portal_chronicle_username
psw = Config.portal_chronicle_password

patient = pytest.data.get_patient_first_last_name('patient_info')
PDS_service_name = pytest.data.get_service_name('PDS')

fields_data = pytest.data.get_data('Chronicle_Systemic_Therapy_data')
fields_data1=pytest.data.get_data('vocab_for_geonomic_alterations')
fields_data2=pytest.data.get_data('vocab_for_systemic_therapy')
fields_data3=pytest.data.get_data('vocab_for_Surgery_and_Radiation')
fields_data4=pytest.data.get_data('vocab_for_cancerDiagnoses')

pytestmark=pytest.mark.skip(reason="currently not required due to low priority")

@pytest.fixture(scope="function")
def pick_patient_for_chronicle(request, app_test):
    app_test.portal.login(username, psw)
    app_test.portal.navigate_to(PDS_service_name)
    app_test.finder.find_and_pick_patient(patient)
    yield
    app_test.driver.close()

@pytest.mark.p4
@pytest.mark.p3
def test_vocab_finder_cancer(app_test, pick_patient_for_chronicle, test_info):
    """
    Chronicle -  Vocabs - Finder - Cancer Diagnosis
    """
    app_test.navigation.refresh_page()
    log.info("Test Started- Chronicle -  Vocabs - Finder - Cancer Diagnosis")
    app_test.chronicle_cancer_diagnosis.click_Add_Another_for_Cancer_Diagnosis()
    app_test.navigation.hide_header()
    app_test.navigation.hide_footer()
    app_test.chronicle_cancer_diagnosis.primarySite_type_and_verify_vocab()
    app_test.chronicle_cancer_diagnosis.primarySite_type_and_verify_empty_result()

    app_test.chronicle_cancer_diagnosis.histology_type_and_verify_vocab()
    app_test.chronicle_cancer_diagnosis.histology_type_and_verify_empty_result()

    app_test.chronicle_cancer_diagnosis.tumorType_type_and_verify_vocab()
    #time.sleep(3)


    app_test.chronicle_cancer_diagnosis.cT_type_and_verify_vocab()
    app_test.chronicle_cancer_diagnosis.cT_type_and_verify_empty_result()

    app_test.chronicle_cancer_diagnosis.cN_type_and_verify_vocab()
    app_test.chronicle_cancer_diagnosis.cN_type_and_verify_empty_result()

    app_test.chronicle_cancer_diagnosis.cM_type_and_verify_vocab()
    app_test.chronicle_cancer_diagnosis.cM_type_and_verify_empty_result()

    app_test.chronicle_cancer_diagnosis.cStageGroup_type_and_verify_vocab()
    app_test.chronicle_cancer_diagnosis.cStageGroup_type_and_verify_empty_result()

    app_test.chronicle_cancer_diagnosis.pT_type_and_verify_vocab()
    app_test.chronicle_cancer_diagnosis.pT_type_and_verify_empty_result()

    app_test.chronicle_cancer_diagnosis.pN_type_and_verify_vocab()
    app_test.chronicle_cancer_diagnosis.pN_type_and_verify_empty_result()

    app_test.chronicle_cancer_diagnosis.pM_type_and_verify_vocab()
    app_test.chronicle_cancer_diagnosis.pM_type_and_verify_empty_result()

    app_test.chronicle_cancer_diagnosis.pStageGroup_type_and_verify_vocab()
    app_test.chronicle_cancer_diagnosis.pStageGroup_type_and_verify_empty_result()

    app_test.chronicle_cancer_diagnosis.distantMetastasis_type_and_verify_vocab()
    log.info("Test Passed")

@pytest.mark.p4
@pytest.mark.p3
def test_vocab_cancer_alterations_surgery(app_test,pick_patient_for_chronicle,test_info):
    """
    Chronicle -  Vocabs - Cancer Diagnosis - Surgery - Genomic Alterations
    """
    log.info("Test Started- test Vocabs - Cancer Diagnosis - Surgery - Genomic Alterations")
    app_test.navigation.refresh_page()       
    #app_test.finder.find_and_pick_patient(patient)
    app_test.chronicle_cancer_diagnosis.click_Add_Another_for_Cancer_Diagnosis()
    app_test.navigation.hide_header()
    app_test.navigation.hide_footer()
    app_test.chronicle_cancer_diagnosis.verify_vocab_for_cancerDiagnoses(dict=fields_data4)

    app_test.chronicle_genomic_alterations.chronicle_tab_Genomic_Alterations()
    app_test.chronicle.click_Add_Another()
    app_test.chronicle_genomic_alterations.verify_vocab_for_genomicAlterations(dict=fields_data1)

    app_test.chronicle_surgery_and_radiation.chronicle_tab_Surgery_and_Radiation()
    app_test.chronicle_surgery_and_radiation.click_Add_Another_for_Cancer_Surgery()
    app_test.chronicle_surgery_and_radiation.verify_vocab_for_Surgery_and_Radiation(dict=fields_data3)

    app_test.chronicle_systemic_therapy.chronicle_tab_Systemic_Therapy()
    app_test.chronicle.click_Add_Another()
    app_test.chronicle_systemic_therapy.verify_vocab_for_Systemic_Therapy(dict=fields_data2)
    log.info("Test Passed")





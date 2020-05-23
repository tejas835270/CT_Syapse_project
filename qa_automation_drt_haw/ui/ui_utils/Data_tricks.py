import json
import os
import pandas as pd

class DataJson:

    def __init__(self):
        self.data_file = 'fixture_data.json'
        self.testdata = self.retrive_data()

    def retrive_data(self):

        temp_file = os.path.abspath(os.path.dirname(__file__) + "/../../test_data/%s" % self.data_file)
        with open(temp_file, "r") as read_file:
            data = json.load(read_file)
        return data

    # purpose to read data from csv file and store it in list "test_data_row_list"
    # data_file is passed from test file
    def retrive_data_from_csv(self, data_file):
        test_data_row_list = list()
        print("datafile=" + data_file)
        temp_file = os.path.abspath(os.path.dirname(__file__) + "/../../test_data/%s" % data_file)
        with open(temp_file, "r"):
            data = pd.read_csv(temp_file, skiprows=0)
            test_data_row_list = data.values.tolist()
        print(test_data_row_list)
        return test_data_row_list
    # ----------------------------------------------------
    #  ------  patients ---------------------------------
    # ----------------------------------------------------
    def get_patient(self,param):
        return self.testdata['patients'][param]


    def get_patient_first_last_name(self, param):
        patient = self.testdata['patients'][param]
        return "%s %s" % (patient['first_name'], patient['last_name'])

    def get_patient_first_name(self, param):
        patient = self.testdata['patients'][param]
        return "%s" % (patient['first_name'])
    # ----------------------------------------------------
    # --------- users ------------------------------------
    # ----------------------------------------------------
    def get_user(self,param):
        return self.testdata['users_dev'][param]

    def get_service_name(self,param):
        return self.testdata['service_names'][param]

    # purpose- to fetch data from 'mtb_create_case_data' tag
    def get_mtb_create_case_data(self, param):
        return self.testdata['mtb_create_case_data'][param]

    #purpose- to fetch data from 'chronicle_fields_test_data' tag
    def get_data(self,param):
        return self.testdata['chronicle_fields_test_data'][param]

    #purpose- to fetch data from 'chronicle_fields_test_data' -> biomarkers tag
    def get_Biomarkers_data(self,param):
        patient = self.testdata['chronicle_fields_test_data'][param]
        return "%s" % (patient['Biomarkers'])

    def get_integration2_org_case_from(self, param):
        return self.testdata['org_cases'][param]

    #ToDo : Handling of same name tags is pending
    def get_json_val(self,root_tag, *tags):
        '''
        Purpose: To get the value from JSON for a given tag
        :param root_tag: This is starting tag for a given JSON
        :param tags: This arg can have multiple tag values.
        :return: Returns the value from JSON based on the tags provided
        '''
        root = self.testdata[root_tag]
        for para in tags:
            root = root[para]
            val = root
        return val

    # def get_minerva_db_credentials(self, param):
    #     return self.testdata['api_dev_db_conn'][param]

    def retrive_data_from_csv_to_list(self, data_file):
        '''
        :purpose: read the data from csv and convert it into the list
        :param data_file:it is passed from test file
        :return: it returns one single list
        '''
        temp_file = os.path.abspath(os.path.dirname(__file__) + "/../../test_data/Data_vocab/%s" % data_file)
        data = []
        with open(temp_file, 'rb') as temp_file:
            for i in temp_file:
                data.append(i.strip().decode("utf-8"))
        return data
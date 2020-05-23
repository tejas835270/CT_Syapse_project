from qa_automation_drt_haw.qa_utils.postgres_utils import Postgres
from qa_automation_drt_haw.settings import Config
from qa_automation_drt_haw.ui.ui_utils.Logs import log

def connect_minerva_db():
    '''
    purpose: Used to connect the minerva data-base
    :return: connection object
    '''

    return Postgres(host=Config.minerva_db_host,port=Config.minerva_db_port,user=Config.minerva_db_user,password=Config.minerva_db_password,dbname=Config.minerva_db_dbname)


def connect_flatstore_db():
    '''
    purpose: Used to connect the flatstore data-base
    :return: connection object
    '''

    return Postgres(host=Config.flatstore_db_host,port=Config.flatstore_db_port,user=Config.flatstore_db_user,password=Config.flatstore_db_password,dbname=Config.flatstore_db_dbname)

def connect_mdx_db():
    '''
    purpose: Used to connect the mdx data-base
    :return: connection object
    '''
    return Postgres(host=Config.mdx_db_host,port=Config.mdx_db_port,user=Config.mdx_db_user,password=Config.mdx_db_password,dbname=Config.mdx_db_dbname)


def get_patient_results_for_organisation(org='aurora'):
    '''
    purpose: This method will provide record-set from flatstore db for give organisation
    :param org: Organisation for which patients are required
    :return: database record-set in dictionary format
    '''
    query = "select record_id from patient where org = '%s'" % org
    db = connect_flatstore_db()
    result = db.get_query_response_dict_format(query)
    del db
    return result

def get_case_id_when_meeting_date_asc_sorted():
    """
     This function returns the Case Id when Meeting date is sorted in Ascending Order
    """
    global db
    query = "select external_case_id,(case_record #>> '{}')::jsonb ->'mtbMeetingInfo'->>'meetingDate' as meetingDate " \
            "from mtb_case  where organization = 'aurora' and case_status ='real-save' order by " \
            "(case_record #>> '{}')::jsonb ->'mtbMeetingInfo'->>'meetingDate' asc nulls first,created_date asc limit 1;"
    try:
        db = connect_minerva_db()
        log.info("Connection with Database is successful")
    except:
        log.error("Issue with the Database connection")
        assert False,"Issue with the Database connection"
    result = db.get_query_response_dict_format(sql_query=query)
    log.info("Query Result is %s" % result)
    del db
    return get_single_value_from_particular_field(result, "external_case_id")


def get_case_id_when_meeting_date_desc_sorted():
    """
    This function returns the Case Id when Meeting date is sorted in Descending Order
    """
    query = "select external_case_id,(case_record #>> '{}')::jsonb ->'mtbMeetingInfo'->>'meetingDate' as meetingDate " \
            "from mtb_case  where organization = 'aurora' and case_status ='real-save' order by " \
            "(case_record #>> '{}')::jsonb ->'mtbMeetingInfo'->>'meetingDate' desc nulls last,created_date desc limit 1;"
    try:
        db = connect_minerva_db()
        log.info("Connection with Database is successful")
    except:
        log.error("Issue with the Database connection")
        assert False, "Issue with the Database connection"
    result = db.get_query_response_dict_format(sql_query=query)
    log.info("Query Result is %s" % result)
    del db
    return get_single_value_from_particular_field(result, "external_case_id")


def get_patient_last_name_with_max_count():
    '''
    purpose: This method will provide patient last name having maximum count
    :return: database record-set in dictionary format
    '''
    query = '''select search_last_name,count(*) "No of patients" from patient where search_last_name is not null Group By search_last_name order by count(*) desc limit 1'''
    db = connect_flatstore_db()
    result = db.get_query_response_dict_format(sql_query=query)
    del db
    return get_single_value_from_particular_field(result,"search_last_name")


def get_single_value_from_particular_field(db_result_dictionary_form,column_name):
    '''
    purpose: This generic method is used to fetch the value for a given column name from the database result set
    :param db_result_dictionary_form: data base result set in dictionary format
    :param column_name: column name for which value is to be retrieved
    :return: single value for a given column
    '''
    if type(db_result_dictionary_form).__name__ == 'list' or type(db_result_dictionary_form).__name__ == 'dict':
        if type(db_result_dictionary_form).__name__ == 'list':
            return db_result_dictionary_form[0].get(column_name)
        elif type(db_result_dictionary_form).__name__ == 'dict':
            return db_result_dictionary_form.get(column_name)
    else:
        log.error("unable to get the value")


def query_db(db_name,query,max_result_count=10):
    '''
    purpose: This is a generic method to get the databases from required database for a given query
    :param db_name: data base name in which query needs to be performed
    :param query: sql query to fetch the result
    :param max_result_count: From the fetched result for the query, the count of records will get returned will be equal to "max_result_count"
    :return: data base result in dictionary format
    '''
    global db
    if str(db_name).lower() == "minerva":
        db = connect_minerva_db()
    elif str(db_name).lower() == "flatstore":
        db = connect_flatstore_db()
    elif str(db_name).lower() == "mdx":
        db = connect_mdx_db()
    else:
        print("error - Invalid db name0")

    result = db.get_query_response_dict_format(query,max_result_count)
    del db
    return result
















def main():
   print("hello")


if __name__ == "__main__":
        main()
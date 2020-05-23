# qa-automation-drt-haw
repo for UI and API automation covering all respective services belonging to Hustle and Workflow


#### Filtering tests to run
This test framework supports filtering tests to run for given test suite(s) and or test level(s)

Test Levels
* Tests are assigned priorities to correspond to test levels:
  * p0: mark a test as priority 0 (smoke test level)
  * p1: mark a test as priority 1 (sanity test level)
  * p2: mark a test as priority 2 (short regression test level)
  * p3: mark a test as priority 3 (corner case or unlikely scenarios)
* A test is assigned a priority via a pytest marker, e.g. @pytest.mark.p0
 
#### Logging mode
This test framework supports logging modes.  Default is info, but can be overwritten from command line.

Logging modes:
* info
* debug
* warning
* error

#### Illustrations

#### How to Run UI tests
Section below illustrates the procedure to run UI tests locally as well as via jenkins:
est Levels
* Steps to run UI tests locally:
  * Requirements: Python 3.7.x, Selenium 3.x, Licensed Pycharm Professional Version (2018 above), pytest, pipenv
  * Steps:
    * brew install pipenv
    * brew cask install chromedriver
    * clone your project from git repo (qa-automation-drt-haw)
    * cd qa-automation-drt-haw/ui/qa_tests/ , right click on any folder that you want to run and click on run(by setting up       pytest test configuration)
    * pipenv shell
    * pipenv install (this will install all dependencies from the piplock file)
    * pytest qa_automation_drt_haw/ui/qa_tests/<test_folder>/<test_name> eg 
      pytest qa_automation_drt_haw/ui/qa_tests/chronicle/chronicle_general_test.py 
    

#### How to Run UI tests from Docker
    git clone the repo
    cd <repo>
    ./bin/run <test type> <test_env> <test> <test_suite>
    Example ./bin/run ui dev portal-web portal_web_test.py
* test types can be ui or api (mandatory parameter)
* test_env is optional parameter. It can be dev or stg. By default is dev
* test is an optional parameter which needs to be provided in case you want to run a specifc component (@ folder level)
* test_suite is an optional parameter which needs to be provided in case you want to run a specifc file within component

* Imp : Sequence of parameters need to be maintained

#### Prerequisites to run API tests locally (via IDE or docker)
* For cluster based API services, port-forwarding is required in order to access those services
* Below steps need to be performed to port-forward on given environment (dev or stg)
* For following services, port-forwarding is required - minerva-service,routing-service,flatstore-patient,chronicle-service
* Below commands needs to be executed for port-forwarding as per the required environment (env = dev or stg)
    * k8s-auth <env> (Note - Authentication code will be generated. Copy that and paste it back in the terminal)
    * kubectl -n <env> port-forward svc/minerva-service 4001:443
    * kubectl -n <env> port-forward svc/routing-service 4000:443
    * kubectl -n <env> port-forward svc/flatstore-patient 8445:443
    * kubectl -n <env> port-forward svc/chronicle-service 8446:443

#### How to Run UI tests from Docker using .env file 
* copy .env.example under [qa_automation_drt_haw]folder and rename it to  .env file with configurations needed for running tests
* ./bin/build - to build the image
* ./bin/run <test type> <test_env> <test> <test_suite> : to run the tests

#### Prerequisites to run UI tests locally (via IDE or docker)
* For cluster based API services, port-forwarding is required in order to access those services
* Below steps need to be performed to port-forward on given environment (dev or stg)
* Below commands needs to be executed for port-forwarding as per the required environment (env = dev or stg)
    * k8s-auth <env> (Note - Authentication code will be generated. Copy that and paste it back in the terminal)
    * kubectl -n <env> port-forward svc/flatstore-patient 8445:443
    
#### Troubleshooting(if any)

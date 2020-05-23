import os
import time

# This will come into use while executing at command line using pytest command
if os.getenv('ROOT_DIR') is None:
    if 'qa-automation' in os.getcwd():
        os.environ['ROOT_DIR'] = os.getcwd().split('/qa-automation')[
                                     0] + '/qa-automation' + os.getcwd().split('/qa-automation')[1].split('/')[0]
        os.environ['REPORT_DIR'] = os.environ['ROOT_DIR'] + '/qa_reports'
    print('local- '+ os.environ['ROOT_DIR'])
    print('local- '+ os.environ['REPORT_DIR'])

import pytest

from qa_automation_drt_haw.ui.model.application import Application
from qa_automation_drt_haw.ui.ui_utils.Data_tricks import DataJson
from qa_automation_drt_haw.ui.ui_utils.Logs import log


# root_dir = '/qa-automation-drt-haw-' + os.environ['ENV']


def create_fixture_app(request):
    print("create driver")
    global env
    env = request.config.getoption("--env")
    # browser = request.config.getoption("--browser")
    print("conftest env")
    print(env)
    fixture = Application(env=env, browser='chrome')
    global driver
    driver = fixture.driver
    fixture.open_home_page()

    def fin():
        print("close driver")
        fixture.destroy()

    request.addfinalizer(fin)
    return fixture

#   Possible values for scope are: function, class, module, package or session
#   https://docs.pytest.org/en/latest/fixture.html
#  -----  module fixtures ---------------------

@pytest.fixture(scope='module')
def app(request):
    print("create APP fixture")

    return create_fixture_app(request)


@pytest.fixture(scope='module')
def app1(request):
    print("create APP fixture")
    return create_fixture_app(request)


@pytest.fixture(scope="module")
def login(request, app):
    print("create login fixture")
    app.session.login(request.module.username, request.module.psw)


# --------  UI tests fixtures ------------------
# -------------------------------------------
#   Fixture functions can accept the request object to introspect the “requesting” test function
@pytest.fixture(scope='function')
def app_test(request):
    return create_fixture_app(request)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    pytest_html = item.config.pluginmanager.getplugin('html')
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()
    # set a report attribute for each phase of a call, which can
    # be "setup", "call", "teardown"
    setattr(item, "rep_" + rep.when, rep)
    # Added implementation for logging details in pytest html report
    extra = getattr(rep, 'extra', [])

    if pytest_html is not None:
        log_test = pytest.log_test
        log_ticket_link = pytest.log_link
        log_screenshot = pytest.log_screenshot

        # Adding test description
        if log_test != "":
            extra.append(pytest_html.extras.text("", name=log_test))
            pytest.log_test = ""

        # Linking given ticket
        #note - For multiple tickets to be linked, it can be done by passing list of tickets
        #eg. link_single_ticket = "Ticket url"
        # link_multiple_ticket = ['Ticket1_url','Ticket2_url']
        if log_ticket_link == "":
            extra.append(pytest_html.extras.url(log_ticket_link, name='Linked Ticket not provided'))
        else:
            if 'list' in type(log_ticket_link).__name__:
                for links in log_ticket_link:
                    extra.append(pytest_html.extras.url(links,name=links))
            else:
                extra.append(pytest_html.extras.url(log_ticket_link, name=log_ticket_link))
        pytest.log_link = ""

        # Linking screen-shot for failed scenarios
        extra.append(pytest_html.extras.url(log_screenshot, name='Screenshot (Available only for Failed UI Test)'))
        # extra.append(pytest_html.extras.image(log_screenshot))
        rep.extra = extra
    return rep


@pytest.fixture(scope='function')
def test_info(request):
    print(f"""\n> BEGIN TEST CASE: {request.function.__name__}""")
    filename = "" + request.function.__name__ + "" + "-" + time.strftime(
        "%d-%m-%Y_%I-%M_%p") + ".png"
    # if os.getenv('PROJECT_DIR') is not None:
    #     path = os.environ['PROJECT_DIR'] + '/qa_reports/Failed_scenarios/'
    # elif 'qa-automation-drt-haw' in os.getcwd():
    #     path = os.getcwd().split(root_dir)[0] + root_dir +'/qa_reports/Failed_scenarios'
    # else:
    #     print('Invalid Project Directory')
    # os.path.abspath("Failed_scenarios")
    path = os.environ['REPORT_DIR'] + '/Failed_scenarios/'
    fullpath = os.path.join(path, filename)

    # Provision for docker path
    # if 'srv' in fullpath:
    #     pytest.log_screenshot = 'qa_reports/Failed_scenarios/'+filename
    # else:
    #     # Provision for local path
    #     pytest.log_screenshot = root_dir + fullpath.split(root_dir, 1)[1]
    pytest.log_screenshot = '/qa-automation-drt-haw/qa_reports/Failed_scenarios/' + filename

    yield

    if request.node.rep_setup.failed:
        print("setting up a test failed!", request.node.nodeid)

    elif request.node.rep_setup.passed:
        if request.node.rep_call.failed:

            print("FAILED")

            if not os.path.exists(path):
                os.makedirs(path)

            try:
                driver.save_screenshot(fullpath)
            except NameError as error:
                log.error('driver not available')
    else:
        print("PASSED")

    print(f"""\n> END TEST CASE: {request.function.__name__}""")
    print("\n\n====================================================================")


def pytest_configure(config):
    pytest.data = DataJson()
    pytest.env = config.getoption('--env')
    pytest.log_test = ""
    pytest.log_link = ""
    pytest.log_screenshot = ""
    if os.getenv('ENV') is None:
        os.environ['ENV'] = pytest.env
    log.info("Working on env - %s" % os.getenv('ENV'))


def pytest_addoption(parser):
    if os.getenv('ENV') is not None:
        temp_env = os.getenv('ENV')
    else:
        temp_env = "dev"

    parser.addoption("--env", action="store", default=temp_env)

"""Console script for qa-automation-db-rocky."""
import click
import pytest
import os
import time

@click.command()
@click.option('component',
              '--component',
              multiple=False,
              type=click.Choice(['mtb-web', 'portal-web', 'chronicle-service', 'flatstore-patient',
                                 'minerva-service', 'oncology-web', 'routing-service', 'tableau','patient-finder','monthly-release']))
@click.option('type',
              '--type',
              multiple=False,
              type=click.Choice(['ui', 'api']))
@click.option('levels',
              '--level',
              multiple=True,
              type=click.Choice(['p0', 'p1', 'p2', 'p3','p4']))
@click.option('suites',
              '--suite',
              multiple=True,
              # type=click.Choice([])
              )
@click.option('log_level',
              '--log_level',
              type=click.Choice(['info', 'debug', 'warning', 'error']))
@click.option('env',
              '--env',
              default='dev',
              type=click.Choice(['dev', 'sqa']))
def main(levels, type, component, suites, log_level, env):

    global report_dir, root_dir

    # Getting values from terminal and processing them
    pytest_component = get_test_component(component)
    pytest_type = get_test_type(type)
    env = 'dev' if not env else env
    timestamp = time.strftime("%d-%m-%Y_%I-%M_%p")

    # For Jenkins
    if 'jenkins' in os.getcwd():
        root_dir = "/srv"
        report_dir = os.getcwd() + '/qa_reports'
    # For docker
    elif 'srv' in os.getcwd():
        root_dir = "/srv"
        report_dir = "/srv/qa_reports"
    # For Local execution
    elif 'qa-automation' in os.getcwd():
        root_dir = os.getcwd().split('/qa-automation')[
                                     0] + '/qa-automation' + os.getcwd().split('/qa-automation')[1].split('/')[0]
        report_dir = root_dir + '/qa_reports'
    else:
        print('Invalid project directory')

    # Defining environment variables which are required in test execution
    os.environ['COMP'] = pytest_component
    os.environ['TYPE'] = pytest_type
    os.environ['TIMESTAMP'] = timestamp
    os.environ['ENV'] = env
    os.environ['ROOT_DIR'] = root_dir
    os.environ['REPORT_DIR'] = report_dir
    print(os.environ['ENV'])

    # Forming report name
    if pytest_component == "":
        html_report_name = "report_" + pytest_type + "_" + timestamp
    else:
        html_report_name = "report_" + pytest_type + "_" + pytest_component + "_" + timestamp

    pytest_args = [
        "-v",
        #"-s",
        f"""--html={os.environ['REPORT_DIR']}/{html_report_name}.html""",
        "--self-contained-html",
        "-rsx",
        "--assert=plain"]

    pytest_levels = get_test_levels(levels)
    pytest_suites = get_test_suites(suites, pytest_component, pytest_type)

    if pytest_levels:
        pytest_args.append(pytest_levels)

    if log_level:
        pytest_args.append(f"--log-cli-level={log_level.upper()}")

    if len(pytest_suites) > 0:
        for pytest_suite in pytest_suites:
            pytest_args.append(pytest_suite)
    elif pytest_component != "":
        pytest_args.append(f"{os.environ['ROOT_DIR']}/qa_automation_drt_haw/{pytest_type}/qa_tests/{pytest_component}")
    else:
        pytest_args.append(f"{os.environ['ROOT_DIR']}/qa_automation_drt_haw/{pytest_type}/qa_tests")

    print(f"""pytest args: {pytest_args}""")
    pytest.main(pytest_args)


def get_test_levels(levels):
    '''
    :purpose: to fetch the priority/level
    :Description:It reads priority values from settings.py file from where we can change the priorities for sqa and dev environment whenever it is required
    :return: priority/levels
    '''
    from settings import Config
    sqa_level=Config.ui_sqa
    dev_level=Config.ui_dev
    pytest_levels = ""

    if os.getenv('ENV') == 'sqa':
        pytest_levels =(f"""-m {sqa_level}""")
        print(pytest_levels)
    elif os.getenv('ENV') == 'dev':
        for level in dev_level:
            if pytest_levels:
                pytest_levels = pytest_levels + f""" or {level}"""
                print(pytest_levels)
            else:
                pytest_levels = (f"""-m {level}""")
                print(pytest_levels)
    return pytest_levels


def get_test_type(type):
    pytest_type = "api"

    if type is not None:
        pytest_type = f"""{type}"""

    return pytest_type


def get_test_component(component):
    pytest_component = ""

    if component is not None:
        pytest_component = f"""{component}"""

    return pytest_component


def get_test_suites(suites, component, type):
    pytest_suites = []
    # test_dir = os.environ['TESTS']
    for suite in suites:
        pytest_suites.append(f"""{os.environ['ROOT_DIR']}/qa_automation_drt_haw/{type}/qa_tests/{component}/{suite}""")

    return pytest_suites


if __name__ == "__main__":
    main()

import logging
import logging.handlers
import os
import time

# log_folder = os.getcwd()

if os.getenv('TYPE') is not None and os.getenv('COMP') is not None and os.getenv('TIMESTAMP') is not None:
    filename = 'log_' + os.environ['TYPE'] + '_' + os.environ['COMP'] + '_' + os.environ['TIMESTAMP']+ '.log'
else:
    filename = 'log_' + time.strftime("%d-%m-%Y_%I-%M_%p") + '.log'

log_folder = os.environ['REPORT_DIR']

if not os.path.isdir(log_folder):
    print(f'The log {log_folder}')
    os.mkdir(log_folder)

log_filename = log_folder + '/' + filename
print(log_filename)
# log_filename = '/srv/qa_reports' + '/' + filename

log = logging.getLogger()
log.setLevel(logging.INFO)

c_format = logging.Formatter('%(asctime)s: - '
                             'File:- %(filename)s  '
                             'Method:- '
                             '%(''funcName)s - '
                             '%(lineno)d - '
                             '%(levelname)s: -  '
                             '%(''message)s',
                             datefmt='%d-%m-%Y %I:%M:%S')

c_handler = logging.handlers.TimedRotatingFileHandler(log_filename,
                                                      when='midnight',
                                                      # interval=5,
                                                      backupCount=3,
                                                      utc=False)
c_handler.setFormatter(c_format)
log.addHandler(c_handler)

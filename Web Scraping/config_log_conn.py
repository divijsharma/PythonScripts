from configparser import ConfigParser
import psycopg2
import logging as log
from datetime import date
from datetime import datetime
import sys
from static_variables import *


def read_config(file_path, section):
    """
    The function to read the connection parameters from the relevant section in the config file.

    Right now the config file name is hardcoded in the program
    :param file_path: the name of the file that will be read.
    :param section: The section of the file has to be read.
    :return section_content: Dictionary with the section parameters.
    :rtype: Dictionary
    """
    # create parser and read configuration file
    parser = ConfigParser()
    parser.read(file_path)

    section_content = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            section_content[item[0]] = item[1]
    else:
        raise Exception('Error in fetching config in read_config method. {0} not found in \
         {1}'.format(section, file_path))

    return section_content


def create_connection(config_dict):
    """
    The function to create the connect based on the parameters in dictionary. The function uses
    psycopg2 package for making the connection.
    :param config_dict: Dictionary containing the parameters of connection
    :return: Cursor
    :rtype: Database Cursor Object
    """
    host = config_dict.get('host')
    port = config_dict.get('port')
    database = config_dict.get('database')
    user = config_dict.get('user')
    password = config_dict.get('password')
    conn = ''
    try:
        conn = psycopg2.connect(database=database
                                , user=user
                                , password=password
                                , host=host
                                , port=port
                                )
    except psycopg2.OperationalError as e:
        log.error(str(e).rstrip())

    if conn:
        log.info('Database Connection is returned Successfully')
        log.info('Host = %s', host)
        log.info('Database = %s', database)
    else:
        log.critical('Database Connection was not successful. Terminating program!!!')
        log.critical('Host = %s', host)
        log.critical('Database = %s', database)
        sys.exit()

    return conn


def get_folder_file_details(config_dict):
    """
    The function to get the folder and file details from the dictionary passed.
    The function will ignore all other keys and fetch details of only folder and file keys.
    The current run date is also attached to the file name. These files are usually output files.
    :param config_dict: The dictionary with config details
    :return: folder and file names
    :rtype: str
    """
    folder = config_dict.get(FOLDER)
    file = config_dict.get(FILE)
    file = str(date.today()) + '_' + file
    return folder, file


def set_logging_basics(config_dict, pgm_name):
    """
    The function to set the logging information.
    :param pgm_name: Name of the program that will be put in the log
    :param config_dict: dictionary with details of configuration
    :return: None
    """
    folder, file = get_folder_file_details(config_dict)
    level = config_dict.get('level')
    log.basicConfig(filename=folder + file
                    , filemode='a'
                    , format='%(name)s - %(levelname)s - %(message)s'
                    , level=level)
    log.info('--------------- NEW RUN %s -----------------', pgm_name)
    log.info('Log Date = %s', datetime.now())


def get_state_list(config_dict):
    """
    The function to get the list of slates
    :param config_dict: dictionary with details of configuration
    :return: list of states
    :rtype: list
    """
    return list(config_dict.get(STATE).split(","))


def get_url_details(config_dict):
    """
    The function to get the API URL
    :param config_dict: dictionary with details of configuration
    :return: API URL
    :rtype: str
    """
    return config_dict.get(URL)


def get_login_details(config_dict):
    """
    The function to get the login details
    :param config_dict
    :return: user name, password and org name
    :rtype: str
    """
    return config_dict.get(USER), config_dict.get(PASSWORD), config_dict.get(ORG_NAME)


def get_pmjay_url(config_dict):
    return config_dict.get(PMJAY_URL_FIRST), config_dict.get(PMJAY_URL_SECOND), config_dict.get(PMJAY_URL_THIRD)

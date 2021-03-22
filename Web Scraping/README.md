**Web Scraping - FTP Files.ipynb** - How to read data from page and download files form FTP server

**pmjay_hsp_scraping.py** - This script has following details - 
1. How to fetch data by calling API
2. How to deal with pagination

In this case the API does not need authentication. If you are interested in knowing how to call API that requires authentication refer to https://divijsharma.medium.com/calling-apis-with-authentication-token-5e4412bd75b5

**config_log_conn.py** - This python script has functions for reading config files, making connections and initializing logs. This file is imported in multiple programs that require these functions.

**main_config.ini** - All the sensitive information like user name, password, schema, folder name have been redacted. This is the main config file. All the configurations are present in this file. This file is used as driver file. It has to be used in conjunction with static_variables file because this file has the name of all the sections of config files. Config file is created to minimize the hardcoding and to ensure that the environmental variables can be changed without a need to deploy the program again. For more details see https://divijsharma.medium.com/config-files-and-logging-a7b4cc377fd5

**static_variables.py** - This file has the name of all static variables. The file is created separately to ensure that all static variables are stored in a single file. Also, in case of any change in the name of section in config file the program with business logic need not be touched at all and only place the relevant change is required is the static variable file, this reduces the human error. This file is used in conjunction with config file. All the sensitive information like folder details have been redacted.

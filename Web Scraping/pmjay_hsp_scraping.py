import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
import re
from config_log_conn import *

if __name__ == '__main__':
    PGM_NAME = 'pmjay_hsp_scraping.py'
    # Getting the Logging details at the beginning of the program
    set_logging_basics(read_config(MASTER_FOLDER + MASTER_FILE, LOGGER_SECTION), PGM_NAME)

    # Get details of PMJAY hospital output file
    pmjay_hsp_folder, pmjay_hsp_file = get_folder_file_details(read_config(MASTER_FOLDER + MASTER_FILE,
                                                                           PMJAY_HSP_FILE_SECTION))

    # Get PMJAY State lists
    pmjay_state_dict = read_config(MASTER_FOLDER + MASTER_FILE, PMJAY_STATE_SECTION)
    log.info(pmjay_state_dict)

    # Get PMJAY URL Details
    pmjay_url_first, pmjay_url_second, pmjay_url_third = get_pmjay_url(read_config(MASTER_FOLDER + MASTER_FILE,
                                                                                   PMJAY_HSP_URL_SECTION))
    # The data is present between > and <
    MATCH_PATTERN = '>(.*?)<'
    hsp_cols = ['hsp_name', 'hsp_type', 'hsp_add', 'hsp_email', 'hsp_phone', 'hsp_spec', 'hsp_upgrade_spec',
                'hsp_state_min', 'hsp_dist_min', 'hsp_sub_type']

    for state_id in pmjay_state_dict:
        # Create a new dataframe
        hsp_data_df = pd.DataFrame(columns=hsp_cols)

        # Start of page
        page_num = 1

        # Create a different file for each state
        final_hsp_file_name = pmjay_state_dict[state_id] + ' - ' + pmjay_hsp_file

        # Substitute the page number and state_id to get the full URL of hospital details from PMJAY Website.
        pmjay_hsp_full_url = pmjay_url_first + str(page_num) + pmjay_url_second + state_id + pmjay_url_third

        # Get the page and create soup for easier processing
        page = requests.get(pmjay_hsp_full_url)
        soup = bs(page.content, 'lxml')

        # Loop till the end of pages. Last page is identified by 'No Records Found' text.
        # len() == 0 implies 'No Records Found' was not present and which means that page has data.
        while len(soup.body.findAll(text=re.compile(NO_RECORDS))) == 0:
            # Fetch the data related to different tags in separate variables. These variables are lists.
            hsp_names = soup.find_all("td", {"data-title": "Hospital Name"})
            hsp_types = soup.find_all("td", {"data-title": "Hospital Type"})
            hsp_adds = soup.find_all("td", {"data-title": "Hospital Address"})
            hsp_emails = soup.find_all("td", {"data-title": "Hospital E-Mail"})
            hsp_phones = soup.find_all("td", {"data-title": "Hospital Contact"})
            hsp_specs = soup.find_all("td", {"data-title": "Specialities Empanelled"})
            hsp_upgrd_specs = soup.find_all("td", {"data-title": "Specialities Upgraded"})
            hsp_state_mins = soup.find_all("td", {"data-title": "???EMPNL.SateOfMinistryHospital???"})
            hsp_dist_mins = soup.find_all("td", {"data-title": "???EMPNL.DistrictOfMinistryHospital???"})
            hsp_sub_types = soup.find_all("td", {"data-title": "???EMPNL.HospitalSubType???"})

            # Loop through the page. The length of each of above variables will be same. Max 10.
            for index in range(len(hsp_names)):
                # " ".join(str(hsp_adds[index]).split()) removes all unnecessary whitespaces, /t, /n ,/r
                # .strip() removes the leading and trailing spaces
                # This is done to remove all the space characters
                hsp_name = re.search(MATCH_PATTERN, " ".join(str(hsp_names[index]).split())).group(1).strip()
                hsp_type = re.search(MATCH_PATTERN, " ".join(str(hsp_types[index]).split())).group(1).strip()
                hsp_add = re.search(MATCH_PATTERN, " ".join(str(hsp_adds[index]).split())).group(1).strip()
                hsp_email = re.search(MATCH_PATTERN, " ".join(str(hsp_emails[index]).split())).group(1).strip()
                hsp_phone = re.search(MATCH_PATTERN, " ".join(str(hsp_phones[index]).split())).group(1).strip()
                hsp_spec = re.search(MATCH_PATTERN, " ".join(str(hsp_specs[index]).split())).group(1).strip()
                hsp_upgrd_spec = re.search(MATCH_PATTERN, " ".join(str(hsp_upgrd_specs[index]).split())).group(
                    1).strip()
                hsp_state_min = re.search(MATCH_PATTERN, " ".join(str(hsp_state_mins[index]).split())).group(1).strip()
                hsp_dist_min = re.search(MATCH_PATTERN, " ".join(str(hsp_dist_mins[index]).split())).group(1).strip()
                hsp_sub_type = re.search(MATCH_PATTERN, " ".join(str(hsp_sub_types[index]).split())).group(1).strip()
                insert_row = [hsp_name, hsp_type, hsp_add, hsp_email, hsp_phone, hsp_spec, hsp_upgrd_spec,
                              hsp_state_min, hsp_dist_min, hsp_sub_type]
                hsp_data_df.loc[len(hsp_data_df)] = insert_row

            log.info('%d page of %s written', page_num, pmjay_state_dict[state_id])

            # Fetch the new page so that len() in while loop will work properly
            page_num = page_num + 1
            pmjay_hsp_full_url = pmjay_url_first + str(page_num) + pmjay_url_second + state_id + pmjay_url_third
            page = requests.get(pmjay_hsp_full_url)
            soup = bs(page.content, 'lxml')

        log.info(hsp_data_df)
        # Export the dataframe to csv
        hsp_data_df.to_csv(path_or_buf=pmjay_hsp_folder + final_hsp_file_name, index=False, header=True, mode='a')
        log.info('%s csv is stored', pmjay_state_dict[state_id])
        # Delete the dataframe because every state will have a separate file.
        del hsp_data_df

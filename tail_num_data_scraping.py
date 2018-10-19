import pandas as pd
from bs4 import BeautifulSoup
import requests
import re


def find_match(t_num, conv_df):
    for i in range(conv_df.shape[0]):
        if conv_df.loc[i, 'old_tail_num'] == t_num:
            return conv_df.loc[i, 'new_tail_num']
        else:
            pass
    return None


def scrape(t_num):
    assert isinstance(t_num, str)
    id_list = {'mfr_name': 'content_lbMfrName',
               'model': 'content_Label7',
               'year': 'content_Label17',
               'cert_year': 'content_lbCertDate',
               'eng_mfr_name': 'content_lbEngMfr',
               'eng_model': 'content_lbEngModel',
               'aircraft_type': 'content_Label11'
               }
    key_list = list(id_list.keys())
    ret_id_list = {'mfr_name': 'content_drptrDeRegAircraft_lbDeRegMfrName_0',
                   'model': 'content_drptrDeRegAircraft_lbDeRegModel_0',
                   'year': 'content_drptrDeRegAircraft_lbDeRegYearMfr_0',
                   'cert_year': 'content_drptrDeRegAircraft_lbDeRegCertDate_0',
                   'eng_mfr_name': 'content_drptrDeRegAircraft_lbDREngMfr_0',
                   'eng_model': 'content_drptrDeRegAircraft_lbDREngModel_0',
                   }
    ret_key_list = list(ret_id_list.keys())

    column_list = ['tail_num']
    column_list.extend(key_list)
    scrape_df = pd.DataFrame(columns=column_list)
    scrape_df.loc[0, 'tail_num'] = t_num
    response = requests.get(
        'https://registry.faa.gov/aircraftinquiry/NNum_Results.aspx'
        '?NNumbertxt=' + t_num
    )
    soup = BeautifulSoup(response.content, "html.parser")
    not_retired = False
    for i in range(3):
        if soup.find('span', id=id_list[key_list[i]]):
            not_retired = True
        else:
            pass

    if not_retired:
        for key in key_list:
            s = soup.find('span', id=id_list[key]).string.strip()
            if s != 'None':
                scrape_df.loc[0, key] = s
            else:
                pass
    else:
        is_dereg = False
        for i in range(3):
            if soup.find('span', id=ret_id_list[ret_key_list[i]]):
                is_dereg = True
            else:
                pass
        if is_dereg:
            for key in ret_key_list:
                s = soup.find('span', id=ret_id_list[key]).string.strip()
                if s != 'None':
                    scrape_df.loc[0, key] = s
                else:
                    pass
        else:
            pass
    if isinstance(scrape_df.loc[0, 'cert_year'], str):
        scrape_df.loc[0, 'cert_year'] = re.search(r'\w+/\w+/(\w+)',
                                                  scrape_df.loc[0, 'cert_year']
                                                  ).group(1).strip()
    else:
        pass
    return scrape_df


if __name__ == "__main__":
    tail_num_df = pd.read_csv('./tail_num/tail_num_list.csv')
    tail_num_convert = pd.read_csv('./tail_num/tail_num_convert.csv')
    tail_num_list = tail_num_df['tail_num'].tolist()
    df = pd.DataFrame()
    for tail_num in tail_num_list:
        # tail num has to be converted
        if isinstance(find_match(tail_num, tail_num_convert), str):
            result = scrape(find_match(tail_num, tail_num_convert))
            result.loc[0, 'tail_num'] = tail_num
            df = pd.concat([df, result], ignore_index=True)
        else:
            df = pd.concat([df, scrape(tail_num)], ignore_index=True)
    df.to_csv('./tail_num/new_all_tail_num.csv', index=False)
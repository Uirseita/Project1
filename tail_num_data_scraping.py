import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests
import re
tail_num_2016 = pd.Series(df2016['TAIL_NUM'].unique())
tail_num_2017 = pd.Series(df2017['TAIL_NUM'].unique())
tail_num = pd.concat(
    [tail_num_2016, tail_num_2017], ignore_index=True).unique()
tail_num_df = pd.DataFrame()
# create a new DataFrame for tail num
tail_num_df['tail_num'] = tail_num
tail_num = list(tail_num)
mfr_name = []
model = []
year = []
eng_mfr_name = []
eng_model = []
for url in tail_num:
    if isinstance(url, str):
        response = requests.get(
            'https://registry.faa.gov/aircraftinquiry/NNum_Results.aspx'
            '?NNumbertxt=' + url
        )
        soup = BeautifulSoup(response.content, "html.parser")
        # determine if the planes has retired
        if soup.find('span', id='content_lbMfrName') or \
                soup.find('span', id='content_Label7') or \
                soup.find('span', id='content_Label17'):
            # determine if there is a MFR name
            if soup.find('span', id='content_lbMfrName').string != 'None':
                mfr_name.append(soup.find(
                    'span', id='content_lbMfrName'
                ).string.strip())
            else:
                mfr_name.append(np.nan)
            # determine if there is a model
            if soup.find('span', id='content_Label7').string != 'None':
                model.append(soup.find(
                    'span', id='content_Label7'
                ).string.strip())
            else:
                model.append(np.nan)
            # determine if there is a MFR year
            if soup.find('span', id='content_Label17').string != 'None':
                year.append(int(soup.find(
                    'span', id='content_Label17'
                ).string.strip()))
            # use the year in Certificate Issue Date
            elif soup.find('span', id='content_lbCertDate').string != 'None':
                year.append(int(re.search(
                    r'\w+/\w+/(\w+)', soup.find(
                        'span', id='content_lbCertDate'
                    ).string
                ).group(1).strip()))
            else:
                 year.append(np.nan)
            # determine if there is an eng mfr name
            if soup.find('span', id='content_lbEngMfr').string != 'None':
                eng_mfr_name.append(soup.find(
                    'span', id='content_lbEngMfr'
                ).string.strip())
            else:
                eng_mfr_name.append(np.nan)
            # determine if there is an eng model
            if soup.find('span', id='content_lbEngModel').string != 'None':
                eng_model.append(soup.find(
                    'span', id='content_lbEngModel'
                ).string.strip())
            else:
                eng_model.append(np.nan)
        # the plane has retired
        elif soup.find(
                'span', id='content_drptrDeRegAircraft_lbDeRegMfrName_0'
        ) or soup.find(
            'span', id='content_drptrDeRegAircraft_lbDeRegModel_0'
        ) or soup.find(
            'span', id='content_drptrDeRegAircraft_lbDeRegYearMfr_0'
        ):
            if soup.find(
                    'span', id='content_drptrDeRegAircraft_lbDeRegMfrName_0'
            ).string != 'None':
                mfr_name.append(soup.find(
                    'span', id='content_drptrDeRegAircraft_lbDeRegMfrName_0'
                ).string.strip())
            else:
                mfr_name.append(np.nan)
            # determine if there is a model
            if soup.find(
                    'span', id='content_drptrDeRegAircraft_lbDeRegModel_0'
            ).string != 'None':
                model.append(soup.find(
                    'span', id='content_drptrDeRegAircraft_lbDeRegModel_0'
                ).string.strip())
            else:
                model.append(np.nan)
            # determine if there is a MFR year
            if soup.find(
                    'span', id='content_drptrDeRegAircraft_lbDeRegYearMfr_0'
            ).string != 'None':
                year.append(int(soup.find(
                    'span', id='content_drptrDeRegAircraft_lbDeRegYearMfr_0'
                ).string.strip()))
            # use the year in Certificate Issue Date
            elif soup.find(
                    'span', id='content_drptrDeRegAircraft_lbDeRegCertDate_0'
            ).string != 'None':
                year.append(int(re.search(
                    r'\w+/\w+/(\w+)', soup.find(
                        'span',
                        id='content_drptrDeRegAircraft_lbDeRegCertDate_0'
                    ).string
                ).group(1).strip()))
            else:
                 year.append(np.nan)
            # determine if there is an eng mfr name
            if soup.find(
                    'span', id='content_drptrDeRegAircraft_lbDREngMfr_0'
            ).string != 'None':
                eng_mfr_name.append(soup.find(
                    'span', id='content_drptrDeRegAircraft_lbDREngMfr_0'
                ).string.strip())
            else:
                eng_mfr_name.append(np.nan)
            # determine if there is an eng model
            if soup.find(
                    'span', id='content_drptrDeRegAircraft_lbDREngModel_0'
            ).string != 'None':
                eng_model.append(soup.find(
                    'span', id='content_drptrDeRegAircraft_lbDREngModel_0'
                ).string.strip())
            else:
                eng_model.append(np.nan)
        else:
            mfr_name.append(np.nan)
            model.append(np.nan)
            year.append(np.nan)
            eng_mfr_name.append(np.nan)
            eng_model.append(np.nan)
    else:
        mfr_name.append(np.nan)
        model.append(np.nan)
        year.append(np.nan)
        eng_mfr_name.append(np.nan)
        eng_model.append(np.nan)
tail_num_df['mfr_name'] = mfr_name
tail_num_df['model'] = model
tail_num_df['year'] = year
tail_num_df['eng_mfr_name'] = eng_mfr_name
tail_num_df['eng_model'] = eng_model
tail_num_df.to_csv('tail_num.csv', index=False)

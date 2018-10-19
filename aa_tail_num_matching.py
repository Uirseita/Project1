import numpy as np
import pandas as pd


df = pd.read_csv('flight_data.csv')
tail_num = pd.Series(df['TAIL_NUM'].unique()).dropna()
tail_num_df = pd.DataFrame()
# create a new DataFrame for tail num
tail_num_df['tail_num'] = tail_num
# extract all NxxxAA tail numbers
df_aa = tail_num_df[tail_num_df['tail_num'].str.match(r'^N\w{3}AA$')]
df_tail_num_convert = pd.read_csv('./tail_num/tail_num_convert.csv')
df_aa = df_aa.rename(index=str, columns={"tail_num": "old_tail_num"})
df_aa['new_tail_num'] = np.nan
df_aa = df_aa.reset_index(drop=True)
aa_current = pd.read_csv('./tail_num/aa_current_fleet_tail_num_convert.csv')
# match AA current fleet
for i in range(df_aa.shape[0]):
    for j in range(aa_current.shape[0]):
        if df_aa.loc[i, 'old_tail_num'] \
                == aa_current.loc[j, 'old_tail_num']:
            df_aa.loc[i, 'new_tail_num'] \
                = aa_current.loc[j, 'new_tail_num']
            break
aa_ret = pd.read_csv('./tail_num/aa_retired_fleet_tail_num_convert.csv')
# match AA retire fleet
for i in range(df_aa.shape[0]):
    if not isinstance(df_aa.loc[i, 'new_tail_num'], str):
        for j in range(aa_ret.shape[0]):
            if df_aa.loc[i, 'old_tail_num'] \
                    == aa_ret.loc[j, 'old_tail_num']:
                df_aa.loc[i, 'new_tail_num'] \
                    = aa_ret.loc[j, 'new_tail_num']
                break
# match AA current fleet ignore US/AA in the end
for i in range(df_aa.shape[0]):
    if not isinstance(df_aa.loc[i, 'new_tail_num'], str):
        for j in range(aa_current.shape[0]):
            if df_aa.loc[i, 'old_tail_num'][:-2] \
                    == aa_current.loc[j, 'old_tail_num'][:-2]:
                df_aa.loc[i, 'new_tail_num'] \
                    = aa_current.loc[j, 'new_tail_num']
                break
df_aa = df_aa.dropna(how='any')
df_tail_num_convert = pd.concat([df_tail_num_convert, df_aa])
df_tail_num_convert = df_tail_num_convert.drop_duplicates().reset_index(
    drop=True)
df_tail_num_convert.to_csv('./tail_num/tail_num_convert.csv', index=False)

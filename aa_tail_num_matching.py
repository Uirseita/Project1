import numpy as np
import pandas as pd

# for incorrect or mismatched tail numbers which miss all information
tail_num_df = pd.read_csv('./tail_num/tail_num.csv')
df_missing = tail_num_df[tail_num_df.iloc[:, 1:5].isnull().all(axis=1)]
df_conv_tail_num = pd.DataFrame()
df_conv_tail_num['old_tail_num'] = df_missing['tail_num']
df_conv_tail_num['new_tail_num'] = np.nan
aa_df = pd.read_csv('./tail_num/aa_current_fleet_tail_num_convert.csv')
# match AA current fleet
for i in range(df_conv_tail_num.shape[0]):
    for j in range(aa_df.shape[0]):
        if df_conv_tail_num.loc[i, 'old_tail_num'] \
                == aa_df.loc[j, 'old_tail_num']:
            df_conv_tail_num.loc[i, 'new_tail_num'] \
                = aa_df.loc[j, 'new_tail_num']
            break
aa_ret_df = pd.read_csv('./tail_num/aa_retired_fleet_tail_num_convert.csv')
# match AA retire fleet
for i in range(df_conv_tail_num.shape[0]):
    if not isinstance(df_conv_tail_num.loc[i, 'new_tail_num'], str):
        for j in range(aa_ret_df.shape[0]):
            if df_conv_tail_num.loc[i, 'old_tail_num'] \
                    == aa_ret_df.loc[j, 'old_tail_num']:
                df_conv_tail_num.loc[i, 'new_tail_num'] \
                    = aa_ret_df.loc[j, 'new_tail_num']
                break
# match AA current fleet ignore US/AA in the end
for i in range(df_conv_tail_num.shape[0]):
    if not isinstance(df_conv_tail_num.loc[i, 'new_tail_num'], str):
        for j in range(aa_df.shape[0]):
            if df_conv_tail_num.loc[i, 'old_tail_num'][:-2] \
                    == aa_df.loc[j, 'old_tail_num'][:-2]:
                df_conv_tail_num.loc[i, 'new_tail_num'] \
                    = aa_df.loc[j, 'new_tail_num']
                break
df_conv_tail_num.to_csv('./tail_num/tail_num_convert.csv', index=False)
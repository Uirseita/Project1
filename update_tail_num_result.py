import pandas as pd
import re


def input_function(regex, string, intro='Format error. Please input again.\n'):
    while True:
        t = input(string)
        if re.match(regex, t):
            break
        else:
            print(intro)
            pass
    return t


def update_result_by_input_info(result_df):
    regex_list = {
        'mfr_name': r'^\w+',
        'model': r'^\w+',
        'year': r'^\d{4}$|^Unknown$',
        'cert_year': r'^\d{4}$|^Unknown$',
        'eng_mfr_name': r'^\w+',
        'eng_model': r'^\w+',
        'aircraft_type': r'^Fixed Wing Multi-Engine$|'
                         r'^Fixed Wing Single-Engine$|^Rotorcraft$|^Unknown$'
    }
    key_list = list(regex_list.keys())
    column_list = ['tail_num']
    column_list.extend(key_list)
    while True:
        temp_result = pd.DataFrame(columns=column_list)
        tail_num = input_function(r'^N\w{4,5}$', 'Input the tail number:\n',
                                  intro='Tail number must in '
                                        'the form of Nxxxx or Nxxxxx\n')
        if tail_num not in result_df['tail_num'].tolist():
            print('Tail num not found in the result df\n')
            i = input_function(r'[Yn]',
                               'Add the new tail num to the result? Y/n\n')
            # keep entering other info
            if i == 'n':
                t = input_function(r'[Yn]', 'Input another tail num? Y/n\n')
                if t == 'n':
                    return None
                else:
                    continue
            else:
                temp_result.loc[0, 'tail_num'] = tail_num
        else:
            temp_result = result_df[
                result_df['tail_num'] == tail_num
            ].reset_index(drop=True)
        print('Current info for this tail number:\n')
        print(temp_result, '\n')
        # input other info
        for key in key_list:
            string1 = 'Do you want to update ' + key + ' ? Y/n\n'
            string2 = 'Input a new ' + key + ' or Unknown:\n'
            is_update = input_function(r'[Yn]', string1)
            if is_update == 'n':
                continue
            else:
                temp = input_function(regex_list[key],string2)
                temp_result.loc[0, key] = temp
        if isinstance(temp_result.loc[0, 'year'], str):
            if re.match(r'^\d{4}$', temp_result.loc[0, 'year']):
                temp_result.loc[0, 'year'] = int(temp_result.loc[0, 'year'])
            else:
                pass
        else:
            pass
        if isinstance(temp_result.loc[0, 'cert_year'], str):
            if re.match(r'^\d{4}$', temp_result.loc[0, 'cert_year']):
                temp_result.loc[0, 'cert_year'] = int(
                    temp_result.loc[0, 'cert_year'])
            else:
                pass
        else:
            pass
        print(temp_result, '\n')
        is_update = input_function(r'[Yn]',
                                   'Do you want to update this '
                                   'to result? Y/n\n')
        if is_update == 'Y':
            if tail_num in result_df['tail_num'].tolist():
                result_df = result_df.drop(
                    result_df[result_df['tail_num'] == tail_num].index.values
                ).reset_index(drop=True)
            else:
                pass
            result_df = pd.concat([result_df, temp_result], ignore_index=True)
        else:
            pass

        # determine if want to add anothe tail number
        t = input_function(r'[Yn]', 'Input another tail num? Y/n\n')
        if t == 'n':
            result_df.to_csv('./tail_num/updated_all_tail_num.csv',
                             index=False)
            return result_df
        else:
            continue

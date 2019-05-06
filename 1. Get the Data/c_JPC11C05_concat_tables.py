import unicodedata
import pandas as pd
import re
import glob
import os

main_dir = r"C:\Users\Username\Desktop\End-to-End-Data-Analysis\1. Get the Data\table"
parsed_header_file = r"C:\Users\Username\Desktop\End-to-End-Data-Analysis\1. Get the Data\header\frame.csv"
os.chdir(main_dir)

pattern = '*table.csv'

all_table_files = [os.path.basename(file) for file in glob.glob(os.path.join(main_dir, pattern))]
number_of_files = len(all_table_files)

df_top_half = []
df_bottom_half = []

def blank_rows(df):
    # selects first column, changes type to string,
    # initial type is object
    df[0] = df[0].astype(str)
    df[0] = df[0].map(lambda x: unicodedata.normalize('NFKD', x))
    blank_match = re.compile(r'\s+')
    i = [v for v in df[0].iteritems()]
    for tup in i:
        index, value = tup
        if re.match(blank_match, value):
            df.drop(index, axis=0, inplace=True)
    df.reset_index(inplace=True)
    df.drop(columns='index', inplace=True)

for num in range(0, number_of_files):

    file = str(num) + ' table.csv'
    df = pd.read_csv(file, encoding='ISO-8859-1', header=None)
    blank_rows(df)
    if num % 2 == 0:
        df_top_half.append(df)
    else:
        df_bottom_half.append(df)

def join_frames(list_of_frames):
    # horizontal join of dataframes
    concat_df = pd.concat([obj for obj in list_of_frames], axis=1, join='inner')
    return concat_df

def final_stack_df(top, bottom, headers):
    top_tables = join_frames(top)
    bottom_tables = join_frames(bottom)
    final = pd.concat([top_tables, bottom_tables], axis=0, join='outer')
    headers = pd.read_csv(headers, encoding='ISO-8859-1')
    final.columns = headers.columns
    return final

cmbs = final_stack_df(top=df_top_half, bottom=df_bottom_half, headers=parsed_header_file)
cmbs.to_csv('CMBS Table.csv', index=False, encoding='ISO-8859-1')

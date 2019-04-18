import unicodedata
import pandas as pd
import re
import glob
import os

main_dir = r"C:\Users\Username\Desktop\End to End Data Analysis Project\table"
os.chdir(main_dir)

pattern = '*table.csv'
# is thisss necessary?
all_table_files = [os.path.basename(file) for file in glob.glob(os.path.join(main_dir, pattern))]

df_top_half = []
df_bottom_half = []


def blank_rows(df):
    # first column
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


def is_even(num):
    if num % 2 == 0:
        return True
    else:
        return False


for num in range(0, len(all_table_files)):

    file = str(num) + ' table.csv'
    df = pd.read_csv(file, encoding='ISO-8859-1', na_values='empty', header=None)
    blank_rows(df)
    if is_even(num=num):
        df_top_half.append(df)
    else:
        df_bottom_half.append(df)

cmbs = pd.concat([obj for obj in df_top_half], axis=1, join='inner')
cmbs.to_csv('cmbs_table_even.csv', index=False, encoding='ISO-8859-1')

cmbs2 = pd.concat([obj for obj in df_bottom_half], axis=1, join='inner')
cmbs2.to_csv('cmbs_table_odd.csv', index=False, encoding='ISO-8859-1')

other = pd.concat([cmbs, cmbs2], axis=0, join='outer')
headers = pd.read_csv(r"C:\Users\Username\Desktop\End to End Data Analysis Project\header\frame.csv", encoding='ISO-8859-1')

headers.columns = [re.sub(r'_\d', ' ', col) for col in headers.columns]
headers.columns = [re.sub(r'\s+', ' ', col) for col in headers.columns]
headers.columns = [val.strip() for val in headers.columns]

other.columns = headers.columns

other.to_csv('jpc11c05.csv', index=False, encoding='ISO-8859-1')

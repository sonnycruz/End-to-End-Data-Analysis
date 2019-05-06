import pandas as pd
import os
import re

main_dir = r'C:\Users\Username\Desktop\Python\End-to-End-Data-Analysis\1. Get the Data\table'
file = 'CMBS Table.csv'

os.chdir(main_dir)

cmbs = pd.read_csv(file, encoding='ISO-8859-1')

# Delete extra Loan & Seller columns
loan_seller_cols = [val for val in cmbs.columns.values if re.search('(^Loan\s#|^Seller|^Property\sName)', val)][3:]

for col in loan_seller_cols:
    cmbs.drop(columns=col, axis=1, inplace=True)

# Regex to edit headers
regex_dict = {'_\d': '', '\(.+\)+': '', '#': '', '%': '', r'\/' : '', '\s\s+': ' ', '^\s+': '', '\s+$': ''}

for key, value in regex_dict.items():
    cmbs.columns = [re.sub(key, value, col) for col in cmbs.columns]

# Delete 
for col in list(cmbs.columns.values):
    try:
        if cmbs[col].str.normalize('NFKD').str.match('  ').all():
            cmbs.drop(columns=col, axis=1, inplace=True)
    except AttributeError:
            continue

cmbs.to_csv('CMBS Final.csv', index=False, encoding='ISO-8859-1')

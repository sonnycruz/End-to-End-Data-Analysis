from collections import Counter
import unicodedata
import numpy as np
import os
import csv
import pandas as pd
import glob
import re

main_dir = r"C:\Users\User_Name\Desktop\End to End Data Analysis Project\header"
os.chdir(main_dir)

pattern = '*header.csv'
all_header_files = [os.path.basename(file) for file in glob.glob(os.path.join(main_dir, pattern))]

def is_word(value):
        if re.search(pattern=r'\w', string=value):
                return True
        else:
                return False

def load_headers(filename):
    # Load CSV file count number of header rows.
    # Return Pandas DF with correct headers.

    f = open(filename)
    reader = csv.reader(f)

    # create dictionary to parse headers
    # as well as get correct number of
    # header rows 
    header_rows = 0
    header_dict = {}
    for line in reader:
        new_line = [unicodedata.normalize('NFKD', value) for value in line]
        header_dict[header_rows] = new_line
        header_rows += 1

    # length of main header for reference
    main_header = header_dict[len(header_dict)-1]
    main_header_len = len(main_header)

    # if column name is text and has more than one
    # instance of it in a given row, append a
    # random number to it to differentiate it
    # this is necessary so that multi-index
    # is all tuples and not strings.
    for row_ind, row in header_dict.items():
            counts = Counter(row)
            for word in enumerate(row):
                    word_index = word[0]
                    word_text = word[1]
                    if is_word(word_text) and counts[word_text] > 1:
                            header_dict[row_ind][word_index] = word_text + '_' + str(np.random.randint(10))
                    else:
                            continue

    filename = filename.strip('.csv') + '_' + 'parsed' + '.csv'
    
    with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(header_dict.values())
    
    df = pd.read_csv(filename, encoding='ISO-8859-1', header=[number for number in range(header_rows)],
                     na_values='empty')
    
    df.columns = [' '.join(col).strip() for col in df.columns.values]

    return df

all_header_values = []
for num in range(0, 20, 2):
        file = str(num) + ' header.csv'
        df = load_headers(file)
        all_header_values.append(df)

frame = pd.concat([value for value in all_header_values], axis=1)

print(frame)
frame.to_csv('frame.csv', index=False)

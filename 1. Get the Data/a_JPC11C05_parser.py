from bs4 import BeautifulSoup
from bs4 import Tag
import pandas as pd
import shutil
import glob
import csv
import re
import os


working_dir = r'C:\Users\Username\Desktop\End-to-End-Data-Analysis\1. Get the Data'
os.chdir(working_dir)
filename = r"C:\Users\Username\Desktop\End-to-End-Data-Analysis\1. Get the Data\Raw Dataset\JPC11C05.html"

with open(filename) as sec:
    soup = BeautifulSoup(sec, 'lxml')

tables = [
    table for table in soup.findAll("table") if 'border' not in table.attrs
    ]

table_count = len(tables)


def is_header(tag, keyword=r'bold'):
    # returns bs4.element.Tag or None
    return tag.find("font", {"style": re.compile(keyword)})


def unwanted_header(tag, colspan_limit=2):
    colspan_obj = tag.find("td", {"colspan": re.compile(r"\d+")})
    if colspan_obj:
        colspan_val = int(colspan_obj['colspan'])
        if colspan_val > colspan_limit:
            return True
        else:
            return False


def is_good_header(tag):
    if is_header(tag) and not unwanted_header(tag):
        return True
    else:
        return False


def cells_same_colspan(colspan_dict):
    # reduce colspan dict values
    max_colspan_per_row = [max(val) for val in colspan_dict.values()]
    if max(max_colspan_per_row) == 1:
        return True
    else:
        return False


def nested_colspan_dict(colspan_dict):
    nested_colspan_obj = {
        key: [colspan_tuple for colspan_tuple in enumerate(value)]
        for key, value in colspan_dict.items()}
    return nested_colspan_obj


def colspans_to_fix(nested_colspan):
    for key, value in nested_colspan.items():
        for tupl in value:
            #tuples are (colspan_index, colspan_value)
            if tupl[1] != 1:
                # key = row number
                # tuple = (index_of_cell, colspan_value_for_cell)
                yield {key: tupl}


def write_rows(current_table, filename, data):
    with open(str(current_table) + filename + '.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        # if row avoids blank rows
        writer.writerows(row for row in data.values() if row)


def headers_tables(name, file_path=os.getcwd()):
    if not os.path.exists(name):
        os.mkdir(name)
    pattern = '*' + name + '.csv'
    file_list = [file for file in glob.glob(os.path.join(file_path, pattern))]
    for file in file_list:
        shutil.move(file, name)


for i in range(table_count):

    table = tables[i]
    header_rows = {'headers': {}, 'tdata': {}}
    colspan = {}
    line_count = 0
    
    for row in table.findAll("tr"):
        colspan[line_count] = [int(td_tag['colspan'])
                               if 'colspan' in td_tag.attrs else 1
                               for td_tag in row.findAll('td')]
        if is_good_header(row) and i % 2 == 0:
            header_rows['headers'][line_count] = [data.font.text
                                                  if isinstance(data.font, Tag) else ''
                                                  for data in row.findAll('td')]
            line_count += 1
        elif is_header(row) is None:
            header_rows['tdata'][line_count] = [data.font.text
                                                if isinstance(data.font, Tag) else ''
                                                for data in row.findAll('td')]
            line_count += 1
        else:
            continue
    if cells_same_colspan(colspan):
        write_rows(current_table=i, filename=' header', data=header_rows['headers'])
        write_rows(current_table=i, filename=' table', data=header_rows['tdata'])
    else:
        nested_cs = nested_colspan_dict(colspan)
        bad_colspans = [cs for cs in colspans_to_fix(nested_cs)]
        headers_only = [h for h in header_rows['headers']]
        for colspan_dict in bad_colspans:
            for k, v in colspan_dict.items():
                row_index = k
                colspan_ind, colspan_val = v
                colspan_minus_one = colspan_val - 1
                index_for_insert = colspan_ind + 1
                if row_index in headers_only:
                    headers = header_rows['headers'][row_index]
                    for insert in range(colspan_minus_one):
                        headers.insert(index_for_insert, '')
                else:
                    rows = header_rows['tdata'][row_index]
                    for insert in range(colspan_minus_one):
                        rows.insert(index_for_insert, '')
        write_rows(current_table=i, filename=' header', data=header_rows['headers'])
        write_rows(current_table=i, filename=' table', data=header_rows['tdata'])


headers_tables('header')
headers_tables('table')

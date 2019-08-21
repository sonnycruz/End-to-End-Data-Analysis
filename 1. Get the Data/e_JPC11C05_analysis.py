import matplotlib.pyplot as plt
from numpy import nan as NA
import pandas as pd
import numpy
import os

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
path = r'C:\Users\Username\Desktop\End-to-End-Data-Analysis\1. Get the Data\table'
file = 'CMBS New Final.csv'

df = pd.read_csv(os.path.join(path,file), encoding='ISO-8859-1')

# Commands to see df characteristics
df.shape

df.info()

df.columns.values

# save columns to a textfile:
indx_cols = []
for tupl in enumerate(df.columns.values):
      indx, col = tupl
      indx_cols.append(str(indx) + ' ' + col)
np.savetxt("cmbs cols.txt", indx_cols, fmt="%s")

# Null Value Counts Per Column.
#normalize link: https://docs.python.org/3/library/unicodedata.html#unicodedata.normalize
str_dtypes = df.select_dtypes(include=['object'])
utf_encoded = str_dtypes.apply(lambda x: x.str.normalize('NFKD'), axis=1)
df.loc[:, [col for col in utf_encoded.columns]] = utf_encoded
df.replace('  ', NA, inplace=True)
round(df.count() / df.shape[0], 2)

# Datatypes of Each Column
df.dtypes

# Data Type Conversion Functions
def currency(df, col):
      df[col] = df[col].replace("[$,()%]", "", regex=True).astype(float)

currency(df, 'Current Balance')

def date_convert(df, col):
      df[col] = pd.to_datetime(df[col], infer_datetime_format=True, errors='coerce')

date_convert(df, 'Final Mat Date')

# Create subset of data with only loans
df['Loan Count'] = df['Loan'].astype(str)
loans = df.loc[df['Loan Count'].str.endswith('0'),:]

# Bar Graph
prop_dict = loans.groupby('Property Type')['Number of Properties'].sum().to_dict()

def cmbs_bars(dict_data, title, ylim_low, ylim_high, ylabel, y_thousands=True,
              text_message='', text_c1=0, text_c2=0, style='seaborn-bright',
              bar_color='darkblue', xtick_rotation=0, xtick_font='large',
              facecolor='lightgray', grid_line_style='-', grid_line_width='0.5',
              grid_color='gray'):

      data = sorted(dict_data.items(), key=lambda x: x[1], reverse=True)
      data_keys = [key[0] for key in data]
      data_index = range(len(data_keys))
      data_values = [value[1] for value in data]
      plt.style.use(style)
      fig = plt.figure()
      ax1 = fig.add_subplot(111)
      ax1.bar(data_index, data_values, align='center', color=bar_color)
      plt.xticks(data_index, data_keys, rotation=xtick_rotation,
                 fontsize=xtick_font)
      ax1.set_ylim(ylim_low, ylim_high)
      plt.ylabel(ylabel)
      plt.text(text_c1, text_c2, text_message)
      plt.title(title)
      ax1.set_facecolor(color=facecolor)
      ax1.grid()
      ax1.grid(linestyle=grid_line_style, linewidth=grid_line_width,
               color=grid_color)
      ax1.set_axisbelow(True)
      if y_thousands:
            ax1.get_yaxis().set_major_formatter(
                plt.FuncFormatter(
                    lambda x, loc: "{:,}".format(int(x))))
      plt.show()


cmbs_bars(dict_data=prop_dict, title='Number of Properties by Property Type', ylim_low=0,
          ylim_high=200, ylabel='Number of Properties', xtick_rotation=11, xtick_font=8.5)

# Summary statistics
def cmbs_stats(df):
      num_loans = df.shape[0]
      num_props = df['Number of Properties'].sum()
      prop_type_count = df.groupby('Property Type')['Number of Properties'].sum()
      prop_dist = round(prop_type_count / num_props, 2).to_dict()
      dsc_describe = df['UW NOI DSCR'].agg(['mean', 'median', 'std', 'max', 'min'])
      print('\n')
      print("Number of Loans: {}".format(str(num_loans)))
      print('\n')
      print("Number of Properties: {}".format(str(num_props)))
      print('\n')
      print("Percent of Properties by Property Type: \n")
      for key, value in prop_dist.items():
            print(key + ": " + str(value))
      print('\n')
      print("Total Loan Balance of Pool: \n{}".format(df['Current Balance'].sum()))
      print('\n')
      print("UW NOI DSCR: \n{}".format(dsc_describe))
 

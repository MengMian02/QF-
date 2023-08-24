import os
import pandas as pd
from technical import *

def technical_indicator(table):

    # =======以下计算指标的公式，可以修改
    # 遍历过去的40个数据，find the lowest value. (前40行没有adjusted low values)
    table['LOW_N'] = table['最低价_复权'].rolling(20).min()
    table['HIGH_N'] = table['最高价_复权'].rolling(20).max()

    # When Adjusted closing price == Lowest adjusted price, RSV == 0
    table['RSV'] = (table['收盘价_复权'] - table['LOW_N']) / (table['HIGH_N'] - table['LOW_N']) * 100
    # Exponential moving average for RSV for the past 2 periods
    table['K'] = table['RSV'].ewm(span=(3-1), adjust=False).mean()
    # Exponential moving average for K for the past 2 values
    table['D'] = table['K'].ewm(span=(3-1), adjust=False).mean()


    # =======以下计算交易信号，可以修改
    # 金叉死叉信号
    # K values are more sensitive to recent changes
    # D values are the exponential moving average of K, so K crosses over D indicates a buy signal
    table.loc[(table['K'].shift(1) <= table['D'].shift(1)) & (table['K'] > table['D']), 'signal'] = 1  # 买入信号
    table.loc[(table['K'].shift(1) >= table['D'].shift(1)) & (table['K'] < table['D']), 'signal'] = 0  # 卖出信号


    return table


csv_file = 'sz301312.csv'
file_path = os.path.abspath(os.path.dirname(__file__)) + '\股票数据' + '\\' + csv_file

print(file_path) 

table = pd.read_csv(file_path, encoding = 'utf-8-sig', parse_dates= ['交易日期'], dayfirst=False)


technical_indicator(table)

table.to_csv(file_path, index = False)

with open(file_path, 'r', encoding = 'utf-8') as file:
    content = file.read()

with open(file_path, 'w', encoding = 'utf-8-sig') as file:
    file.write(content)



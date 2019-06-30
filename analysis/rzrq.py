# -*- coding:utf-8 -*-
import os
import sys
import pandas as pd
import numpy as np
sys.path.append("tushare")
import tushare.stock.trading as td
import tushare.stock.indictor as idt
from tushare.stock.fundamental import get_stock_basics
from tushare.stock.reference import moneyflow_hsgt
from tushare.util import dateu as du
import dfplot.dfplot as dfplot
from analysis.basics import get_stock_cn_name

csv_dir='csv'
pci_dir='pic'

def get__hist_rzrq_ma(code=None):
    rzrq_file = '%s/rzrq_%s_%s.csv'%(csv_dir,code,get_stock_cn_name(int(code)))
    rzrq_ma_file = '%s/rzrq_ma_%s_%s.csv'%(csv_dir,code,get_stock_cn_name(int(code)))
    try:
        if os.path.exists(rzrq_file) is True:
            df = pd.read_csv(rzrq_file, encoding='GBK')
        else:
            df = td.get_hist_rzrq(code)
            df.to_csv(rzrq_file, encoding='GBK')
    except Exception as er:
        print(str(er))
    else:
        print(df.tail())
        df = df.sort_values('date', ascending=True)
        df = df.reset_index(drop=True)
        ma3 = idt.ma(df, 3, val_name='rzjme')
        ma5 = idt.ma(df, 5, val_name='rzjme')
        ma10 = idt.ma(df, 10, val_name='rzjme')
        ma20 = idt.ma(df, 20, val_name='rzjme')
        ma60 = idt.ma(df, 60, val_name='rzjme')
        ma120 = idt.ma(df, 120, val_name='rzjme')
        ma250 = idt.ma(df, 250, val_name='rzjme')
        df['ma3'] = ma3
        df['ma5'] = ma5
        df['ma10'] = ma10
        df['ma20'] = ma20
        df['ma60'] = ma60
        df['ma120'] = ma120
        df['ma250'] = ma250
        df_to_csv = df.sort_values('date', ascending=False)
        df_to_csv.reset_index(drop=True)
        df_to_csv.to_csv(rzrq_ma_file, encoding='GBK')
        return df

if __name__ == '__main__':
    df = get__hist_rzrq_ma('002415')
    print(df.head())

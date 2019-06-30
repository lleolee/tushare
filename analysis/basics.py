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

csv_dir='csv'
pci_dir='pic'
def get_stock_cn_name(code=None):
    base_file = '%s/base.csv' % csv_dir
    df = pd.DataFrame
    try:
        if os.path.exists(base_file) is True:
            df = pd.read_csv(base_file, encoding='GBK')
        else:
            df = get_stock_basics()
            df.to_csv(base_file, encoding='GBK')
    except Exception as er:
        print(str(er))
    else:
        names = df.loc[df['code'] == code]['name'].values
        if(len(names) > 0):
            return names[0]
        else:
            return ''
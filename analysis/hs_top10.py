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

def get_hist_top10_hs():
    sh_top10_file = '%s/sh_top10.csv' % csv_dir
    sz_top10_file = '%s/sz_top10.csv' % csv_dir
    hs_top10_file = '%s/hs_top10.csv' % csv_dir
    df_sh = pd.DataFrame()
    df_sz = pd.DataFrame()
    df_hs = pd.DataFrame()
    try:
        if os.path.exists(hs_top10_file) is True:
            df_hs = pd.read_csv(hs_top10_file, encoding='GBK')
        else:
            if os.path.exists(sh_top10_file) is True:
                df_sh = pd.read_csv(sh_top10_file, encoding='GBK')
            else:
                df_sh = td.get_hist_top10_sh()
                df_sh.to_csv(sh_top10_file, encoding='GBK')
            if os.path.exists(sz_top10_file) is True:
                df_sz = pd.read_csv(sz_top10_file, encoding='GBK')
            else:
                df_sz = td.get_hist_top10_sz()
                df_sz.to_csv(sz_top10_file, encoding='GBK')

            df_hs = df_sh
            df_hs = df_hs.append(df_sz)
            df_hs = df_hs.reset_index(drop=True)
            print(df_hs)
            df_hs = df_hs.sort_values(by=['HqDate','BuyAndSellAmount'],ascending=False)
            print(df_hs)
            df_hs = df_hs.reset_index(drop=True)
            df_hs.to_csv(hs_top10_file, encoding='GBK')
    except Exception as er:
        print(str(er))
    else:

        return df_hs

def get_hist_top_hs_pure_latest_n(data=None, count=1):
    df = data
    if len(df)<=20*count and len(df) > 20:
        df =df
    elif len(df)<=20 :
        return None
    else:
        df = df[0:20*count]
    df = df[['StockCode', 'Pure']].groupby(['StockCode']).sum()
    df = df.sort_values(by=['Pure'], ascending=False)
    hs_pure_top_file = '%s/hs_pure_top_latest_%d.csv' % (csv_dir,count)
    values = []
    for index, row in df.iterrows():
        values.append(get_stock_cn_name(int(index)))
    names = np.asarray(values)
    df.insert(0, 'Name', names)
    df.to_csv(hs_pure_top_file, encoding='GBK')
    return df

def get_hist_top_hs_amount_latest_n(data=None, count=1):
    df = data
    if len(df) <= 20 * count and len(df) > 20:
        df = df
    elif len(df) <= 20:
        return None
    else:
        df = df[0:20 * count]
    hs_amount_top_file = '%s/hs_amount_top_latest_%d.csv' % (csv_dir,count)
    values = []
    df = df[['StockCode', 'BuyAndSellAmount']].groupby(['StockCode']).sum()
    df = df.sort_values(by=['BuyAndSellAmount'], ascending=False)
    for index, row in df.iterrows():
        values.append(get_stock_cn_name(int(index)))
    names = np.asarray(values)
    df.insert(0, 'Name', names)
    df.to_csv(hs_amount_top_file, encoding='GBK')
    return df

def moneyflow_hsgt_detail():
    hsgt_file = '%s/moneyflow_hsgt.csv' % (csv_dir)
    hsgt_detail_file = '%s/moneyflow_hsgt_detail.csv' % (csv_dir)
    df = pd.DataFrame()
    try:
        if os.path.exists(hsgt_file) is True:
            df = pd.read_csv(hsgt_file, encoding='GBK',index_col=0)
        else:
            df = moneyflow_hsgt()
            df.to_csv(hsgt_file, encoding='GBK')
    except Exception as er:
        print(str(er))
    else:
        print(df.tail())
        df = df.sort_values('date', ascending=True)
        df = df.reset_index(drop=True)
        nmma3 = idt.ma(df, 3, val_name='north_money')
        nmma5 = idt.ma(df, 5, val_name='north_money')
        nmma10 = idt.ma(df, 10, val_name='north_money')
        nmma20 = idt.ma(df, 20, val_name='north_money')
        nmma60 = idt.ma(df, 60, val_name='north_money')
        nmma120 = idt.ma(df, 120, val_name='north_money')
        nmma250 = idt.ma(df, 250, val_name='north_money')
        df['nmma3'] = nmma3
        df['nmma5'] = nmma5
        df['nmma10'] = nmma10
        df['nmma20'] = nmma20
        df['nmma60'] = nmma60
        df['nmma120'] = nmma120
        df['nmma250'] = nmma250
        df_to_csv = df.sort_values('date', ascending=False)
        df_to_csv.reset_index(drop=True)
        df_to_csv.to_csv(hsgt_detail_file, encoding='GBK')
        return df
if __name__ == '__main__':
    df = get_hist_top10_hs()
    df_pure_1 = get_hist_top_hs_pure_latest_n(df)
    df_pure_3 = get_hist_top_hs_pure_latest_n(df,3)
    df_pure_5 = get_hist_top_hs_pure_latest_n(df,5)
    df_pure_20 = get_hist_top_hs_pure_latest_n(df,20)
    df_pure_60 = get_hist_top_hs_pure_latest_n(df,60)
    df_pure_120 = get_hist_top_hs_pure_latest_n(df,120)
    df_pure_250 = get_hist_top_hs_pure_latest_n(df,250)
    df_amoun_1 = get_hist_top_hs_amount_latest_n(df)
    df_amoun_3 = get_hist_top_hs_amount_latest_n(df,3)
    df_amoun_5 = get_hist_top_hs_amount_latest_n(df, 5)
    df_amoun_10 = get_hist_top_hs_amount_latest_n(df, 10)
    df_amoun_20 = get_hist_top_hs_amount_latest_n(df, 20)
    df_amoun_60 = get_hist_top_hs_amount_latest_n(df, 60)
    df_amoun_120 = get_hist_top_hs_amount_latest_n(df, 120)
    df_amoun_250 = get_hist_top_hs_amount_latest_n(df, 250)
    df = moneyflow_hsgt_detail()
    print(df.tail())
    df_plot = df.tail(60)
    df_plot = df_plot[
        ['date', 'north_money', 'nmma3', 'nmma5', 'nmma10', 'nmma20', 'nmma60', 'nmma120',
         'nmma250']]
    dfplot.plot(df_plot, "%s/hsflow.png"%(pci_dir))
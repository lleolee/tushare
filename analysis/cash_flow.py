# -*- coding:utf-8 -*-
import os
import sys
import pandas as pd
sys.path.append("tushare")
import tushare.stock.trading as td
import tushare.stock.indictor as idt
import dfplot.dfplot as dfplot
from analysis.basics import get_stock_cn_name

csv_dir='csv'
pci_dir='pic'

def cash_flow_anaysis(code=None,day=60):
    file = '%s/hist_cash_%s_%s.csv'%(csv_dir,code,get_stock_cn_name(int(code)))
    df = pd.DataFrame()
    try:
        if os.path.exists(file) is True:
            df = pd.DataFrame.from_csv(file)
        else:
            df = td.get_hist_cash(code)
            df.to_csv(file)
    except Exception as er:
        print(str(er))
    else:
        print("can't get DataFrame")
    df = df.reset_index(drop=True)
    df = df.sort_index(ascending=False)
    df = df.reset_index(drop=True)
    print(df.tail())
    ifma3 = idt.ma(df,3,val_name='pureinflow')
    ifma5 = idt.ma(df, 5, val_name='pureinflow')
    ifma10 = idt.ma(df, 10, val_name='pureinflow')
    ifma20 = idt.ma(df,20, val_name='pureinflow')
    ifma60 = idt.ma(df, 60, val_name='pureinflow')
    ifma120 = idt.ma(df, 120, val_name='pureinflow')
    ifma250 = idt.ma(df, 250, val_name='pureinflow')
    df['ifma3'] = ifma3
    df['ifma5'] = ifma5
    df['ifma10'] = ifma10
    df['ifma20'] = ifma20
    df['ifma60'] = ifma60
    df['ifma120'] = ifma120
    df['ifma250'] = ifma250

    mifma3 = idt.ma(df, 3, val_name='puremaininflow')
    mifma5 = idt.ma(df, 5, val_name='puremaininflow')
    mifma10 = idt.ma(df, 10, val_name='puremaininflow')
    mifma20 = idt.ma(df, 20, val_name='puremaininflow')
    mifma60 = idt.ma(df, 60, val_name='puremaininflow')
    mifma120 = idt.ma(df, 120, val_name='puremaininflow')
    mifma250 = idt.ma(df, 250, val_name='puremaininflow')
    df['mifma3'] = mifma3
    df['mifma5'] = mifma5
    df['mifma10'] = mifma10
    df['mifma20'] = mifma20
    df['mifma60'] = mifma60
    df['mifma120'] = mifma120
    df['mifma250'] = mifma250

    merge_file = '%s/hist_cash_%s_%s_merge.csv' % (csv_dir, code,get_stock_cn_name(int(code)))
    df.to_csv(merge_file)
    merge_desc_file = '%s/hist_cash_%s_%s_merge_desc.csv' % (csv_dir, code,get_stock_cn_name(int(code)))
    df_desc = df.sort_index(ascending=False)
    df_desc = df_desc.reset_index(drop=True)
    df_desc.to_csv(merge_desc_file)

    df = df.tail(day)
    # df_cashflow = df[['date','inflow','outflow','pureinflow','ifma3','ifma5','ifma10','ifma20','ifma60','ifma120','ifma250']]
    df_cashflow = df[
        ['date', 'pureinflow', 'ifma3', 'ifma5', 'ifma10', 'ifma20', 'ifma60', 'ifma120',
         'ifma250']]
    # df_cashflow[['outflow']] = -df_cashflow[['outflow']]
    dfplot.plot(df_cashflow, "%s/cashflow_%s_%s.png"%(pci_dir,code,get_stock_cn_name(int(code))))
    # df_cashflow = df[['date', 'maininflow', 'mainoutflow', 'puremaininflow','mifma3','mifma5','mifma10','mifma20','mifma60','mifma120','mifma250']]
    df_cashflow = df[
        ['date', 'puremaininflow', 'mifma3', 'mifma5', 'mifma10', 'mifma20', 'mifma60',
         'mifma120', 'mifma250']]
    # df_cashflow[['mainoutflow']] = -df_cashflow[['mainoutflow']]
    dfplot.plot(df_cashflow, "%s/maincashflow_%s_%s.png"%(pci_dir,code,get_stock_cn_name(int(code))))
    df_close = df[['date','close']]
    dfplot.plot(df_close, "%s/close_%s_%s.png"%(pci_dir,code,get_stock_cn_name(int(code))))


def main():
    code = ['000423']
    day = 60
    for i in range(len(code)):
        cash_flow_anaysis(code[i],day)


if __name__ == '__main__':
    main()

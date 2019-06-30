# -*- coding: utf8 -*-
import matplotlib as mpl
import matplotlib.pyplot as plt
import datetime

def plot(df=None, save_path=None):
    #display chinese
    mpl.rcParams['font.sans-serif'] = [u'SimHei']
    mpl.rcParams['axes.unicode_minus'] = False

    x = [datetime.datetime.strptime(str(d), '%Y-%m-%d').date() for d in df['date']]
    col_num=df.columns.size - 1 #date except
    plt.clf()
    fig=plt.figure(1,figsize=(100,30),dpi=200)
    i = 0
    for index, row in df.iteritems():
        if index == 'date':
            continue;
        plt.plot(x,row,label=index)
        plt.grid(True)
        i+=1
        if i>=col_num:
            break
    plt.legend()
    if(save_path is None):
        plt.show()
    else:
        plt.savefig(save_path, dpi=200)

def plot_one(df):
    #display chinese
    mpl.rcParams['font.sans-serif'] = [u'SimHei']
    mpl.rcParams['axes.unicode_minus'] = False

    x = [datetime.datetime.strptime(str(d), '%Y-%m-%d').date() for d in df['date']]
    col_num=df.columns.size - 1 #date except
    fig,axes=plt.subplots(col_num,1)
    i = 0
    for index, row in df.iteritems():
        if index == 'date':
            continue;
        axes[i].plot(x,row)
        axes[i].grid(True)
        i+=1
        if i>=col_num:
            break
    plt.show()

def plot_mult(df):
    mpl.rcParams['font.sans-serif'] = [u'SimHei']
    mpl.rcParams['axes.unicode_minus'] = False

    x = [datetime.datetime.strptime(str(d), '%Y-%m-%d').date() for d in df['date']]
    col_num=df.columns.size
    i = 0
    for index, row in df.iteritems():
        plt.figure(i)
        plt.title(index)
        plt.plot(x,row)
        plt.grid(True)
        i+=1
        if(i>=col_num):
            break
    plt.show()
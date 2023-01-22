import pandas as pd


def summary2csv(s,name=None):
    # summary input as pd 
    if name is not None:
        s.to_csv(name+'.csv',index=False)
    else:
        s.to_csv('summary.csv',index=False)
    

def archive2csv(a,mode,name=None):
    # archive input as pd 
    if name is not None:
        if mode == 'dump':
            a.to_csv(name+'.csv',index=False)
        elif mode == 'update':
            a.to_csv(name+'.csv',index=False, mode='a', header=False)
    else:
        a.to_csv('summary.csv')

def last_race2csv(lr, name=None):
    # lr input as str 
    if name is not None:
        f = open(name+'.csv','w')
        f.write(lr)
        f.close()
    else:
        f = open('lastrace.csv','w')
        f.write(lr)
        f.close()

def read_summary(name):
    s = pd.read_csv(name+'.csv')
    # s.drop('Unnamed: 0') # erroreous col
    # print(s.columns)
    return s

def read_archive(name):
    a = pd.read_csv(name+'.csv')
    return a


def read_lastrace(name):
    f = open(name+'.csv','r')
    lr = f.read()
    f.close()
    return lr